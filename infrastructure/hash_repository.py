from domain.hash import Hash
from infrastructure.repository import Repository


class HashRepository(Repository):
    def __init__(self, session):
        super(HashRepository, self).__init__(Hash, session)

    def find(self, hash):
        self.entities = self.session.query(self.unit).filter(self.unit.hash == hash)
        return self.entities
