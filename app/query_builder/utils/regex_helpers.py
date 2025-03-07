"""Regular expression utilities for the flexible query builder."""
import re
from typing import Dict, List, Set, Tuple, Optional


def extract_field_aliases(text: str) -> Set[str]:
    """Extract field aliases from a text string.

    Args:
        text: Text to extract aliases from

    Returns:
        Set of alias strings
    """
    field_refs = re.findall(r'([a-z]+)\.([a-zA-Z_]+)', text)
    return {alias for alias, _ in field_refs}


def extract_field_references(text: str) -> List[Tuple[str, str]]:
    """Extract field references from a text string.

    Args:
        text: Text to extract field references from

    Returns:
        List of tuples containing (alias, field_name)
    """
    return re.findall(r'([a-z]+)\.([a-zA-Z_]+)', text)


def parse_condition(condition: str) -> Dict[str, str]:
    """Parse a SQL condition into components.

    Args:
        condition: SQL condition string

    Returns:
        Dictionary containing parsed components:
        - left_side: Left side of the condition
        - operator: Condition operator
        - right_side: Right side of the condition
    """
    # Handle equality conditions
    equality_match = re.match(r'([^=<>!]+)\s*(=|!=|<>|<|<=|>|>=)\s*(.+)', condition)
    if equality_match:
        left, op, right = equality_match.groups()
        return {
            'left_side': left.strip(),
            'operator': op.strip(),
            'right_side': right.strip()
        }

    # Handle IN conditions
    in_match = re.match(r'(.+?)\s+(IN|NOT\s+IN)\s+\((.+)\)', condition, re.IGNORECASE)
    if in_match:
        left, op, values = in_match.groups()
        return {
            'left_side': left.strip(),
            'operator': op.strip().upper(),
            'right_side': f"({values.strip()})"
        }

    # If no match found, return empty components
    return {
        'left_side': condition,
        'operator': '',
        'right_side': ''
    }