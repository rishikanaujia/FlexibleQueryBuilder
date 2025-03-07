"""WHERE clause constructor for the flexible query builder."""
from typing import List, Any

from app.query_builder.constructors.base import ClauseConstructor


class WhereConstructor(ClauseConstructor):
    """Constructor for WHERE clauses."""

    def construct(self, where_conditions: List[str], **kwargs: Any) -> str:
        """Construct a WHERE clause.

        Args:
            where_conditions: List of WHERE conditions
            **kwargs: Additional keyword arguments (unused)

        Returns:
            Constructed WHERE clause string
        """
        if not where_conditions:
            return ""

        return f"WHERE {' AND '.join(where_conditions)}"