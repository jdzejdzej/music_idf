from sqlalchemy import Column, Integer, Float, ForeignKey
from common.base import Base
from domain.hash_calculator import HashCalculator


class Hash(Base):
    __tablename__ = 'hashes'
    id = Column(Integer, primary_key=True)
    song_id = Column(Integer, ForeignKey('songs.id'))
    time = Column(Float)
    hash = Column(Integer)
    hash_calculator = HashCalculator()

    def __init__(self, time, _hash):
        self.time = time
        self.hash = _hash

    @classmethod
    def from_bytes(cls, time, _bytes):
        _hash = cls.hash_calculator.from_bytes(_bytes)
        if _hash is not None:
            return cls(time, _hash)
        return None
