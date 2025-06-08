from contextlib import contextmanager
import re
from typing import Annotated

from fastapi import Depends
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
    def __table_name__(cls):
        return resolve_table_name(cls.__name__)


    # Primary key
    @declared_attr
    def id() -> Mapped[int]:
        return mapped_column(primary_key=True)


@contextmanager
def get_session():
    """Ensures that the session is closed after use."""
    session = SessionLocal()

    try:
        yield session
        session.commit()
    
    except:
        session.rollback()
        raise # contextmanager needs the exception to raise again

    finally:
        session.close()


SessionDep = Annotated[Session, Depends(get_session)]
