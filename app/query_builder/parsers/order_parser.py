"""ORDER BY clause parser for the flexible query builder."""
from typing import Any

from app.query_builder.parsers.base import ParserInterface
from app.utils.constants import FIELD_MAPPINGS


class OrderByParser(ParserInterface):
    """Parser for ORDER BY parameters."""

    def can_parse(self, key: str) -> bool:
        """Check if this parser can handle the given parameter key."""
        return key == "orderBy"

    def parse(self, key: str, value: str, builder: Any) -> None:
        """Parse an ORDER BY parameter and update the builder state."""
        fields = value.split(',')
        for field in fields:
            field = field.strip()
            if ':' in field:
                field_name, direction = field.split(':')
                field_name = field_name.strip()
                direction = direction.strip().upper()
                # Map field name if it exists in mapping
                if field_name in FIELD_MAPPINGS:
                    field_name = FIELD_MAPPINGS[field_name]
                builder.order_by_clauses.append(f"{field_name} {direction}")
            else:
                # Default to ASC if no direction specified
                field_name = field.strip()
                if field_name in FIELD_MAPPINGS:
                    field_name = FIELD_MAPPINGS[field_name]
                builder.order_by_clauses.append(f"{field_name} ASC")