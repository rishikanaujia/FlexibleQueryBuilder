"""Factory for creating parameter parsers."""
from typing import Dict, List, Optional, Any

from app.query_builder.parsers.base import ParserInterface
from app.query_builder.parsers.select_parser import SelectParser
from app.query_builder.parsers.group_parser import GroupByParser
from app.query_builder.parsers.order_parser import OrderByParser
from app.query_builder.parsers.filter_parser import FilterParser


class LimitOffsetParser(ParserInterface):
    """Parser for LIMIT and OFFSET parameters."""

    def can_parse(self, key: str) -> bool:
        """Check if this parser can handle the given parameter key."""
        return key in ["limit", "offset"]

    def parse(self, key: str, value: str, builder: Any) -> None:
        """Parse a LIMIT or OFFSET parameter and update the builder state."""
        if key == "limit":
            builder.limit_value = int(value)
        elif key == "offset":
            builder.offset_value = int(value)


class RequestParserFactory:
    """Factory for creating appropriate parameter parsers."""

    def __init__(self):
        """Initialize the parser factory with all available parsers."""
        self.parsers: List[ParserInterface] = [
            SelectParser(),
            GroupByParser(),
            OrderByParser(),
            LimitOffsetParser(),
            FilterParser()  # FilterParser should be last as it's the most generic
        ]

    def get_parser(self, key: str) -> Optional[ParserInterface]:
        """Get the appropriate parser for a parameter key."""
        for parser in self.parsers:
            if parser.can_parse(key):
                return parser
        return None