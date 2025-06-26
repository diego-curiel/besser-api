from datetime import datetime
from typing import Annotated, Optional

from pydantic import AfterValidator, BaseModel, Field
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from besser.models import TimestampMixin, datetime_now_factory
from besser.database.core import Base
from .validation import valid_char_string, valid_product_code

# Database model
class Product(Base, TimestampMixin):
    code: Mapped[str] = mapped_column(nullable=False)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    replacement_cost: Mapped[float] = mapped_column(default=0, nullable=False)
    profit_margin: Mapped[float] = mapped_column(default=0, nullable=False)
    stock_available: Mapped[int] = mapped_column(default=0, nullable=False)
    
    def __repr__(self) -> str:
        return f"Product(id:{self.id}, code:{self.code}, name:{self.name})"

# Base pydantic model
class BaseProduct(BaseModel):
    code: Annotated[str, AfterValidator(valid_product_code)] 
    name: Annotated[str, AfterValidator(valid_char_string)] = Field(
        max_length=120
    )
    replacement_cost: float = Field(default=0, ge=0)
    profit_margin: float = Field(default=0, ge=0)
    stock_available: int = Field(default=0, ge=0)
    created_at: datetime = Field(default_factory=datetime_now_factory)

# Pydantic model to create and update products
class ProductCreate(BaseProduct):
    pass

# Pydantic model to show data to the client
class ProductPublic(BaseProduct):
    id: int

# Pydantic model to patch products
class ProductPatch(BaseModel):
    code: Annotated[Optional[str], AfterValidator(valid_product_code)] = None
    name: Annotated[Optional[str], AfterValidator(valid_char_string)] = Field(
        default=None, max_length=120
    )
    replacement_cost: Optional[float] = None
    profit_margin: Optional[float] = None
    stock_available: Optional[float] = None
    created_at: Optional[datetime] = None
