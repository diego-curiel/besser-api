import re


def valid_product_code(value: str) -> str:
    """ Validator for product codes."""
    # Match any pattern of numbers and characters
    pattern = re.compile(r"^[\d\w]*$")

    if not pattern.match(value):
        raise ValueError(
            f"{value} can not contain special charactes",
        )

    return value


def valid_char_string(value: str) -> str:
    """The permitted characters are: A-Z, a-z, 0-9, *+-_"""
    pattern = re.compile(r"^[\d\wáéíóúüÁÉÍÓÚÜñÑ*+_\-().\s]*$")

    if not pattern.match(value):
        raise ValueError(
            f"Invalid characters at {value}, the permitted special charactes are '* + - _ ( ) .' and spaces."
        )

    return value
