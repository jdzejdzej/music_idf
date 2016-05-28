from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from common.base import Base
from numpy import little_endian

from domain.hash import Hash


class Song(Base):
    __tablename__ = 'songs'
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    artist = Column(String(50))
    chunks = relationship('Hash', cascade='all, delete-orphan')

    def __init__(self, name, artist, chunks):
        self.name = name
        self.artist = artist
        self.chunks = chunks

    @classmethod
    def from_stream(cls, name, artist, stream):
        chunks = []
        time = 0.0
        output = stream.read(4096)
        while output.frames:
            _bytes = output.to_bytes(not little_endian, True)
            if len(_bytes):
                _hash = Hash.from_bytes(time, _bytes)
                if _hash is not None:
                    chunks.append(_hash)
            time += output.frames / float(stream.sample_rate)
            output = stream.read(4096)
        return cls(name, artist, chunks)
