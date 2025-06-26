from pydantic import ValidationError
import pytest


def test_product_create_invalid_code():
    from besser.product.models import ProductCreate


    t_code = "abc123**"
    t_name = "Tangerines"

    with pytest.raises(ValidationError) as excinfo:
        t_product = ProductCreate(
            code=t_code, # The code must be alpha numeric only
            name=t_name,
        )

        assert not t_product, "Code validation failed!"

    first_error = excinfo.value.errors()[0]
    assert first_error.get("input") == t_code, "Exception not raised"
    assert first_error.get("loc") == ("code",), "Exception not raised"


def test_product_create_invalid_name():
    from besser.product.models import ProductCreate


    t_code = "abc123"
    t_name = "Toyota Corolla 96 <Clutch>"

    with pytest.raises(ValidationError) as excinfo:
        t_product = ProductCreate(
            code=t_code,
            name=t_name, # The name can only contain certain special characters
        )

        assert not t_product, "Name validation failed!"
