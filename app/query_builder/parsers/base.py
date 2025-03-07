"""Base parser interface for the flexible query builder."""
from abc import ABC, abstractmethod
from typing import Any


class ParserInterface(ABC):
    """Interface for parameter parsers."""

    @abstractmethod
    def can_parse(self, key: str) -> bool:
        """Check if this parser can handle the given parameter key.

        Args:
            key: Parameter key to check

        Returns:
            True if this parser can handle the key, False otherwise
        """
        pass

    @abstractmethod
    def parse(self, key: str, value: str, builder: Any) -> None:
        """Parse a parameter and update the builder state.

        Args:
            key: Parameter key
            value: Parameter value
            builder: FlexibleQueryBuilder instance to update
        """
        pass