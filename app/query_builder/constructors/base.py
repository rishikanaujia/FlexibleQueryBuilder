"""Base constructor for SQL clauses."""
from abc import ABC, abstractmethod
from typing import Any


class ClauseConstructor(ABC):
    """Base interface for SQL clause constructors."""

    def __init__(self, schema: str, base_table: str, base_alias: str):
        """Initialize the clause constructor.

        Args:
            schema: Database schema name
            base_table: Base table name
            base_alias: Base table alias
        """
        self.schema = schema
        self.base_table = base_table
        self.base_alias = base_alias

    @abstractmethod
    def construct(self, *args: Any, **kwargs: Any) -> str:
        """Construct a SQL clause.

        Args:
            *args: Variable positional arguments
            **kwargs: Variable keyword arguments

        Returns:
            Constructed SQL clause string
        """
        pass