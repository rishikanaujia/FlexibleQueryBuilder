"""GROUP BY clause parser for the flexible query builder."""
from typing import Any

from app.query_builder.parsers.base import ParserInterface
from app.utils.constants import FIELD_MAPPINGS


class GroupByParser(ParserInterface):
    """Parser for GROUP BY parameters."""

    def can_parse(self, key: str) -> bool:
        """Check if this parser can handle the given parameter key."""
        return key == "groupBy"

    def parse(self, key: str, value: str, builder: Any) -> None:
        """Parse a GROUP BY parameter and update the builder state."""
        fields = value.split(',')
        for field in fields:
            field = field.strip()
            # Map to actual field name if exists in mapping
            mapped_field = FIELD_MAPPINGS.get(field, field)

            # Add to select if not already there
            if mapped_field not in builder.select_fields:
                builder.select_fields.append(mapped_field)

            # Add to group by fields
            builder.group_by_fields.append(mapped_field)