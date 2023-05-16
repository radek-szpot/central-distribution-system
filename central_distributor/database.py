from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


Base = declarative_base()


def create_database():
    """Create the SQLite engine and tables"""
    engine = create_engine('sqlite:///inventory.db')
    Base.metadata.create_all(engine)


def get_session():
    """Create a session to interact with the database and return it"""
    engine = create_engine('sqlite:///inventory.db')
    Session = sessionmaker(bind=engine)
    session = Session()
    return session
