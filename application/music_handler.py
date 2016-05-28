import audiotools
import os


class MusicHandler(object):
    def __init__(self):
        pass

    @staticmethod
    def from_file(filename):
        stream = audiotools.open(filename)
        metadata = stream.get_metadata()
        name = metadata.track_name if metadata.track_name is not None else os.path.basename(filename)
        artist = metadata.artist_name if metadata.artist_name is not None else 'unknown artist'
        pcm = stream.to_pcm()
        stream = audiotools.pcmconverter.Averager(pcm)
        return name, artist, stream
