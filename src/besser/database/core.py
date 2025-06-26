from contextlib import contextmanager
import re
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import (
    DeclarativeBase, 
    Mapped, 
    Session, 
    declared_attr, 
    mapped_column, 
    sessionmaker,
)

engine = create_engine("sqlite:///db.sqlite3")

SessionLocal = sessionmaker(bind=engine)


def resolve_table_name(name):
    """Set the table name to its mapped name"""
    names = re.split("(?=[A-Z])", name)
    return "_".join([x.lower() for x in names if x])


class Base(DeclarativeBase):
    @declared_attr.directive
    def __tablename__(cls):
        return resolve_table_name(cls.__name__)


    # Primary key
    @declared_attr
    def id(cls) -> Mapped[int]:
        return mapped_column(primary_key=True)


@contextmanager
def get_session(
    session_maker: sessionmaker[Session],
) -> Generator[Session]:
    """Ensures that the session is closed after use."""

    session = session_maker()

    try:
        yield session
        session.commit()
    
    except:
        session.rollback()
        raise # contextmanager needs the exception to raise again

    finally:
        session.close()


def get_db() -> Generator[Session]:
    with get_session(session_maker=SessionLocal) as session:
        yield session
