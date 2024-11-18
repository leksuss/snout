from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import DeclarativeBase

from src.config import settings


class Base(DeclarativeBase):
    pass


engine = create_engine(settings.DATABASE_URL, echo=False, future=True)
Session = sessionmaker(autoflush=False, bind=engine)

def db_execute(stmt):
    session = Session()
    try:
        session.execute(stmt)
        session.commit()
    except Exception as e:
        session.rollback()
        print(f"An error occurred: {e}")
        raise
    finally:
        session.close()
