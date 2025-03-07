"""FROM clause constructor for the flexible query builder."""
from typing import Any

from app.query_builder.constructors.base import ClauseConstructor


class FromConstructor(ClauseConstructor):
    """Constructor for FROM clauses."""

    def construct(self, **kwargs: Any) -> str:
        """Construct a FROM clause.

        Args:
            **kwargs: Keyword arguments (unused)

        Returns:
            Constructed FROM clause string
        """
        return f"FROM {self.schema}.{self.base_table} {self.base_alias}"