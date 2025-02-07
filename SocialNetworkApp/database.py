from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base

SQLACLHEMY_DATABASE_URL = 'postgresql://postgres:heisenberg@localhost/social_network_db'

engine = create_engine(SQLACLHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()