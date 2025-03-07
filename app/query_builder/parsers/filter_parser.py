"""Filter parser for the flexible query builder."""
from typing import Any

from app.query_builder.parsers.base import ParserInterface
from app.utils.constants import FIELD_MAPPINGS, FILTER_OPERATORS, JOIN_PATHS


class FilterParser(ParserInterface):
    """Parser for filter parameters."""

    def can_parse(self, key: str) -> bool:
        """Check if this parser can handle the given parameter key."""
        # This parser handles any key that:
        # - Is a field mapping
        # - Is a join key
        # - Is not a special parameter (select, groupBy, orderBy, limit, offset)
        special_params = {"select", "groupBy", "orderBy", "limit", "offset"}
        return (
                key in FIELD_MAPPINGS
                or key in self._get_join_keys()
                or (key not in special_params and "." in key)
        )

    def _get_join_keys(self):
        """Get all keys from JOIN_PATHS."""
        return JOIN_PATHS.keys()

    def parse(self, key: str, value: str, builder: Any) -> None:
        """Parse a filter parameter and update the builder state."""
        # Convert key to actual field if in mapping
        field_name = FIELD_MAPPINGS.get(key, key)

        # Check for operators
        for op_prefix, sql_op in FILTER_OPERATORS.items():
            if isinstance(value, str) and value.startswith(f"{op_prefix}:"):
                filter_value = value[len(op_prefix) + 1:]
                builder.where_conditions.append(f"{field_name} {sql_op} '{filter_value}'")
                return

        # Handle comma-separated values (IN clause)
        if isinstance(value, str) and ',' in value:
            values = [f"'{v.strip()}'" for v in value.split(',')]
            builder.where_conditions.append(f"{field_name} IN ({', '.join(values)})")
        else:
            # Default to equality
            builder.where_conditions.append(f"{field_name} = '{value}'")