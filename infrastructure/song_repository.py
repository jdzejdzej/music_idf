from domain.song import Song
from infrastructure.repository import Repository


class SongRepository(Repository):
    def __init__(self, session):
        super(SongRepository, self).__init__(Song, session)

    def find(self, song_id):
        self.entities = self.session.query(self.unit).filter(self.unit.id == song_id)
        return self.entities
