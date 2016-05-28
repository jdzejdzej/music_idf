import os
import audiotools
from application.mic_handler import MicHandler
from application.music_handler import MusicHandler
from common.db_session import SESSION
from domain.hash_calculator import HashCalculator
from domain.song import Song
from infrastructure.hash_repository import HashRepository
from infrastructure.song_repository import SongRepository


class Identifier(object):
    session = SESSION

    def __init__(self):
        self.hash_repository = HashRepository(self.session)
        self.song_repository = SongRepository(self.session)

    def update_database(self, directory):
        music_handler = MusicHandler()
        unsaved_files = []
        for root, bar, files in os.walk(directory):
            for filename in files:
                filename = os.path.join(root, filename)
                try:
                    name, artist, stream = music_handler.from_file(filename)
                    new_song = Song.from_stream(name, artist, stream)
                    self.song_repository.add(new_song)
                    print (" Zanalizowano %s" % filename)
                except audiotools.UnsupportedFile:
                    print (' Pomijam nieobslugiwany format %s' % filename)
                    if filename.endswith('mp3'):
                        unsaved_files.append(filename)
                except Exception, e:
                    unsaved_files.append(filename)
                    print (e)

    def guess(self):
        mic_handler = MicHandler()
        hash_calculator = HashCalculator()
        chunk_chains = {}
        longest_chain = 0
        mic_handler.listen()
        while not mic_handler.empty() or not mic_handler.is_over():
            if mic_handler.qsize() > 20:
                print "Large backlog: %d" % mic_handler.qsize()
            t, data = mic_handler.pop()
            _hash = hash_calculator.from_bytes(data)
            chunks = self.hash_repository.find(_hash)
            for new_hash in chunks:
                handled = False
                for chain in chunk_chains.get(new_hash.song_id, []):
                    if abs((t - chain[1]) - (new_hash.time - chain[2])) < 0.07:
                        chain[1] = t
                        chain[2] = new_hash.time
                        chain[3] += 1
                        if chain[3] > longest_chain:
                            longest_chain = chain[3]
                            song = self.song_repository.find(chain[0])[0]
                            print "current best match: ( %d partial): %d chain len, %s" % (len(chunk_chains), longest_chain, song.name)
                        if chain[3] >= 7:
                            print
                            print 'guessing: '
                            print song.artist, song.name
                            mic_handler.abandoned = True
                            return
                        handled = True
                        break

                if not handled:
                    chunk_chains.setdefault(new_hash.song_id, []).append([new_hash.song_id, t, new_hash.time, 1])
    # def check_timing(self, hash_time, song_time):
