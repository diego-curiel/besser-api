from typing import Annotated

from fastapi import Depends, Query
from sqlalchemy.orm import Session

from database.models import PaginationParams
from database.core import get_db

PaginationQuery = Annotated[
    PaginationParams, 
    Query(
        description="Generic pagination parameters."
    ),
]

SessionDep = Annotated[Session, Depends(get_db)]
