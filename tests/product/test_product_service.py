from fastapi import HTTPException, status
import pytest
from sqlalchemy.orm import Session

from besser.product.models import ProductCreate, ProductPatch


def test_create_product(db_session: Session, product_in: ProductCreate) -> None:
    from besser.product.service import create_product

    product_out = create_product(product_in=product_in, db_session=db_session)

    assert product_out, "The product was not created!"


def test_get_product(db_session: Session, product_in: ProductCreate) -> None:
    from besser.product.service import create_product
    from besser.product.service import get_product

    product = create_product(db_session=db_session, product_in=product_in)
    product_out = get_product(db_session=db_session, product_id=product.id)

    assert product is product_out, "Could not find the product inside the DB!"


def test_get_product_invalid_id(db_session: Session) -> None:
    from besser.product.service import get_product

    # Assuming that the database is empty (Check conftest.py)
    with pytest.raises(HTTPException) as excinfo:
        product = get_product(db_session=db_session, product_id=1)

        assert not product, "The database was not empty, check conftest!"

    # The resulting HTTP status code must be 404, otherwise it is an error
    status_code = excinfo.value.status_code
    assertion_error_msg = "Expected the HTTP status code 404!"

    assert status_code == status.HTTP_404_NOT_FOUND, assertion_error_msg


def test_update_product(
    db_session: Session, 
    product_in: ProductCreate
) -> None:
    from besser.product.service import create_product
    from besser.product.service import update_product

    product = create_product(product_in=product_in, db_session=db_session)

    p_patch = ProductPatch(
        code="amazing2212",
        name="Amazing Product",
    )

    equal_field_err = "Bot products {f} are not different!"
    assert product.code != p_patch.code, equal_field_err.format(f="code")
    assert product.name != p_patch.name, equal_field_err.format(f="name")

    update_product(
        product=product, 
        product_in=p_patch, 
        db_session=db_session
    )

    not_updated_err = "The product {f} was not updated!"
    assert product.code == p_patch.code, not_updated_err.format(f="code")
    assert product.name == p_patch.name, not_updated_err.format(f="name")


def test_delete_product(db_session: Session, product_in: ProductCreate) -> None:
    from besser.product.service import create_product
    from besser.product.service import delete_product
    from besser.product.service import get_product

    product = create_product(db_session=db_session, product_in=product_in)

    deletion_status = delete_product(
        product_id = product.id, db_session=db_session
    )

    assert deletion_status[0]["msg"] == "Product deleted succesfully."

    with pytest.raises(HTTPException) as excinfo:
        t_product = get_product(product_id=product.id, db_session=db_session)

        # Just in case
        assert not t_product, f"{t_product} was not deleted!"

    # The HTTP status code must be 404, otherwise it is an error
    status_code = excinfo.value.status_code

    assertion_error_msg = "The status code after deletion was not HTTP 404!"
    assert status_code == status.HTTP_404_NOT_FOUND, assertion_error_msg




