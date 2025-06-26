from typing import Optional

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from besser.database.service import Paginator
from besser.database.service import PaginationResult, Paginator
from besser.product.models import Product, ProductCreate, ProductPatch


class ProductPagination(PaginationResult):
    items: list[Product]


def create_product(product_in: ProductCreate, db_session: Session) -> Product:
    """
    Creates a new product.
    
    Params:
        product_in (ProductCreate): Product information.
        db_session (Session): Database session.

    Returns:
        Product: Product created in the database.
    """

    product = Product(
        code = product_in.code,
        name = product_in.name,
        replacement_cost = product_in.replacement_cost,
        profit_margin = product_in.profit_margin,
        stock_available = product_in.stock_available,
        created_at = product_in.created_at
    )

    db_session.add(product)

    db_session.commit()

    return product


def get_product(product_id: int, db_session: Session) -> Product:
    """
    Retrieves a product from the database by its ID.

    Params:
        product_id (int): ID of the product to fetch.
        db_session (Session): Database session.

    Returns:
        Product: Product object retrieved by its ID.

    Raises:
        HTTPException: If the product by the given ID does not exist.
    """
    
    product = db_session.get(Product, product_id)

    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=[{"msg": "The product requested does not exist."}]
        )

    return product


def list_products_filter(
    db_session: Session,
    page: int = 1,
    per_page: int = 20,
    code: Optional[str] = None,
    name: Optional[str] = None,
) -> ProductPagination:
    """
    Filter products by a given criteria.

    Params:
        db_session (Session): Database session.
        page (int, default=1): Number of the page to retrieve.
        per_page (int, default=20): Amount of items to retrieve per page.
        code (Optional[str]): Product code to search in the database.
        name (Optional[str]): Product name to search in the database.
    
    Raises:
        ValueError: If the page number is invalid.
        ValueError: If the amount of items per page is exceeded.
        ValueError: If the code passed is invalid.
    
    Returns:
        List[Product]: List of products matching the given code.
    """
    MAX_PER_PAGE = 1000

    stmt = select(Product).order_by(Product.created_at.desc())

    # Filters
    if code:
        stmt = stmt.where(Product.code.ilike(f"^{code}%"))

    if name:
        stmt = stmt.where(Product.name.ilike(f"^{name}%"))

    paginator = Paginator( # This makes a query to the database
        page=page,
        per_page=per_page,
        stmt=stmt,
        db_session=db_session,
        max_per_page=MAX_PER_PAGE,
    )

    return paginator.get_response()


def update_product(
    product: Product, 
    product_in: ProductPatch,
    db_session: Session
) -> Product:
    """
    Update a product with new data.

    Params:
        product (Product): Database Product model.
        product_in (ProductCreate): New data validated by Pydantic.
        db_session (Session): Database session.

    Returns:
        Product: Product object updated with the new data.
    """
    product_data = product_in.model_dump(exclude_unset=True)
    
    product.code = product_data.get("code", product.code)
    product.name = product_data.get("name", product.name)
    product.replacement_cost = product_data.get("replacement_cost",
                                                product.replacement_cost)
    product.profit_margin = product_data.get("profit_margin", 
                                             product.profit_margin)
    product.stock_available = product_data.get("stock_available", 
                                               product.stock_available)
    product.created_at = product_data.get("created_at",
                                          product.created_at)

    db_session.add(product)
    db_session.commit()

    return product


def delete_product(
    product_id: int, 
    db_session: Session
) -> list[dict[str, str]]:
    """
    Shorcut that removes a product from the database.

    Params:
        product_id (int): ID of the product to delete from the datdabase.
        db_session (Session): Database session.

    Returns:
        list[dict[str, str]: A confirmation message upon successful deletion.

    Raises:
        HTTPException: If the product by the given ID does not exist.
    """
    product = get_product(product_id=product_id, db_session=db_session)

    db_session.delete(product)
    db_session.commit()

    return [
        {
            "msg": "Product deleted succesfully.",
        }
    ]

