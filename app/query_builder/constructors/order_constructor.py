"""ORDER BY clause constructor for the flexible query builder."""
from typing import List, Any

from app.query_builder.constructors.base import ClauseConstructor


class OrderByConstructor(ClauseConstructor):
    """Constructor for ORDER BY clauses."""

    def construct(self, order_by_clauses: List[str], **kwargs: Any) -> str:
        """Construct an ORDER BY clause.

        Args:
            order_by_clauses: List of order by expressions
            **kwargs: Additional keyword arguments (unused)

        Returns:
            Constructed ORDER BY clause string
        """
        if not order_by_clauses:
            return ""

        return f"ORDER BY {', '.join(order_by_clauses)}"