"""Validation utilities for the flexible query builder."""
import re
from typing import Set, Optional


def validate_field_name(field_name: str) -> bool:
    """Validate a field name for SQL safety.

    Args:
        field_name: Field name to validate

    Returns:
        True if the field name is valid, False otherwise
    """
    # Check for SQL injection patterns
    if any(pattern in field_name.lower() for pattern in [
        'select', 'insert', 'update', 'delete', 'drop', 'alter', '--', ';'
    ]):
        return False

    # Basic validation pattern for field names
    pattern = r'^[a-zA-Z_][a-zA-Z0-9_]*$'
    return bool(re.match(pattern, field_name))


def validate_alias(alias: str) -> bool:
    """Validate a table alias for SQL safety.

    Args:
        alias: Table alias to validate

    Returns:
        True if the alias is valid, False otherwise
    """
    # Check for SQL injection patterns
    if any(pattern in alias.lower() for pattern in [
        'select', 'insert', 'update', 'delete', 'drop', 'alter', '--', ';'
    ]):
        return False

    # Basic validation pattern for aliases
    pattern = r'^[a-z][a-z0-9_]*$'
    return bool(re.match(pattern, alias))


def validate_order_direction(direction: str) -> bool:
    """Validate an ORDER BY direction.

    Args:
        direction: Direction string to validate

    Returns:
        True if the direction is valid, False otherwise
    """
    return direction.upper() in ['ASC', 'DESC']


def validate_limit_offset(value: Optional[int]) -> bool:
    """Validate a LIMIT or OFFSET value.

    Args:
        value: Value to validate

    Returns:
        True if the value is valid, False otherwise
    """
    if value is None:
        return True

    # Must be a positive integer
    return isinstance(value, int) and value >= 0