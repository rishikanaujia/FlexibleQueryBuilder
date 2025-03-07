"""SELECT clause parser for the flexible query builder."""
from typing import Any

from app.query_builder.parsers.base import ParserInterface
from app.query_builder.utils.formatting import split_and_trim
from app.utils.constants import FIELD_MAPPINGS


class SelectParser(ParserInterface):
    """Parser for SELECT parameters."""

    def can_parse(self, key: str) -> bool:
        """Check if this parser can handle the given parameter key."""
        return key == "select"

    def parse(self, key: str, value: str, builder: Any) -> None:
        """Parse a SELECT parameter and update the builder state."""
        fields = split_and_trim(value)
        for field in fields:
            # Map to actual field name if exists in mapping
            if field in FIELD_MAPPINGS:
                builder.select_fields.append(FIELD_MAPPINGS[field])
            else:
                builder.select_fields.append(field)