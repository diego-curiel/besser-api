from datetime import datetime
from typing import Optional

from besser.product import models as product_models


def ProductCreateFactory(
    code: Optional[str]=None, 
    name: Optional[str]=None,
) -> product_models.ProductCreate:
    return product_models.ProductCreate(
        code=code if code else "123abc",
        name=name if name else "Teapot",
        replacement_cost=19.5,
        profit_margin=12.5,
        stock_available=22,
        created_at=datetime(year=2025, month=6, day=16, hour=7),
    )

