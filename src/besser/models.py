from datetime import datetime, timezone

from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column


class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(default=func.now())


def datetime_now_factory() -> datetime:
    """Creates a datetime instance with the timezone.utc parameter"""
    return datetime.now(timezone.utc)

