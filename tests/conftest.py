from typing import Generator

from pytest import fixture
from sqlalchemy.orm import Session

from besser.database.core import Base, get_session
from besser.product.models import ProductCreate
from .db import engine_testing
from tests.db import SessionTesting
from tests.factory import ProductCreateFactory


@fixture(scope="function")
def db_session() -> Generator[Session]:
    # Create tables
    Base.metadata.create_all(bind=engine_testing)
    # Yield session context manager
    with get_session(session_maker=SessionTesting) as session:
        yield session

    # Drop tables
    Base.metadata.drop_all(bind=engine_testing)


@fixture
def product_in() -> ProductCreate:
    return ProductCreateFactory()


