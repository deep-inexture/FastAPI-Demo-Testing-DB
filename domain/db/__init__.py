import os

from sqlalchemy import create_engine
from sqlalchemy.engine.base import Engine
from sqlalchemy.orm import sessionmaker, declarative_base

from demo_app.database import Base


SQLALCHEMY_DATABASE_URL = os.environ.get('TESTING_DATABASE_URL')
engine: Engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)

# Base = declarative_base()
DBSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def create_db(file: str):
    pass


def init_db():
    Base.metadata.bind = engine
    DBSession.bind = engine
