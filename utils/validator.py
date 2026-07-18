"""Input validation helpers for the retail sales analytics platform."""

import re
from typing import Any


class ValidationError(Exception):
    """Raised when user-provided input fails validation."""


EMAIL_PATTERN = re.compile(r"^[\w\.\-]+@[\w\-]+\.[a-zA-Z]{2,}$")
PHONE_PATTERN = re.compile(r"^\+?[0-9]{7,15}$")


def validate_non_empty_string(value: Any, field_name: str) -> str:
    """Ensure a value is a non-empty string.

    Args:
        value: The value to check.
        field_name: Human-readable field name used in the error message.

    Returns:
        The trimmed, validated string.

    Raises:
        ValidationError: If the value is not a non-empty string.
    """
    if not isinstance(value, str) or not value.strip():
        raise ValidationError(f"{field_name} must be a non-empty string.")
    return value.strip()


def validate_positive_number(value: Any, field_name: str) -> float:
    """Ensure a value is a positive number (int or float).

    Raises:
        ValidationError: If the value is not numeric or is <= 0.
    """
    try:
        number = float(value)
    except (TypeError, ValueError):
        raise ValidationError(f"{field_name} must be a number.")
    if number <= 0:
        raise ValidationError(f"{field_name} must be greater than zero.")
    return number


def validate_non_negative_int(value: Any, field_name: str) -> int:
    """Ensure a value is a non-negative integer.

    Raises:
        ValidationError: If the value is not an integer or is negative.
    """
    try:
        number = int(value)
    except (TypeError, ValueError):
        raise ValidationError(f"{field_name} must be an integer.")
    if number < 0:
        raise ValidationError(f"{field_name} cannot be negative.")
    return number


def validate_email(value: str) -> str:
    """Ensure a string looks like a valid email address.

    Raises:
        ValidationError: If the value is empty or not a valid email shape.
    """
    value = validate_non_empty_string(value, "Email")
    if not EMAIL_PATTERN.match(value):
        raise ValidationError(f"'{value}' is not a valid email address.")
    return value


def validate_phone(value: str) -> str:
    """Ensure a string looks like a valid phone number.

    Raises:
        ValidationError: If the value is empty or not a valid phone shape.
    """
    value = validate_non_empty_string(value, "Phone")
    if not PHONE_PATTERN.match(value):
        raise ValidationError(f"'{value}' is not a valid phone number.")
    return value
