"""Formatting utilities for the flexible query builder."""
from typing import Any, List


def split_and_trim(text: str, delimiter: str = ',') -> List[str]:
    """Split text by delimiter and trim each part.

    Args:
        text: Text to split
        delimiter: Delimiter to split by

    Returns:
        List of trimmed strings
    """
    return [part.strip() for part in text.split(delimiter)]


def format_sql_value(value: Any) -> str:
    """Format a value for SQL based on its type.

    Args:
        value: Value to format

    Returns:
        Formatted SQL value string
    """
    if value is None:
        return "NULL"
    elif isinstance(value, bool):
        return "TRUE" if value else "FALSE"
    elif isinstance(value, (int, float)):
        return str(value)
    else:
        # Escape single quotes by doubling them
        escaped_value = str(value).replace("'", "''")
        return f"'{escaped_value}'"


def format_in_clause(values: List[Any]) -> str:
    """Format a list of values for use in an SQL IN clause.

    Args:
        values: List of values to format

    Returns:
        Formatted SQL IN clause values
    """
    formatted_values = [format_sql_value(value) for value in values]
    return f"({', '.join(formatted_values)})"