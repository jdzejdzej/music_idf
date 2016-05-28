from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine.url import URL
from common.base import Base
from domain.hash import Hash
from domain.song import Song


DATABASE = {
    'drivername': 'postgres',
    'host': 'localhost',
    'port': '5432',
    'username': 'music_idf',
    'password': 'music',
    'database': 'music'
}


def create_session():
    engine = create_engine(URL(**DATABASE))
    Base.metadata.bind = engine
    db_session = sessionmaker(bind=engine)
    return db_session()

SESSION = create_session()
