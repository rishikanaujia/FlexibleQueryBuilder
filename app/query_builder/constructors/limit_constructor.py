"""LIMIT/OFFSET clause constructor for the flexible query builder."""
from typing import Optional, Any

from app.query_builder.constructors.base import ClauseConstructor


class LimitOffsetConstructor(ClauseConstructor):
    """Constructor for LIMIT and OFFSET clauses."""

    def construct(
            self,
            limit_value: Optional[int] = None,
            offset_value: Optional[int] = None,
            **kwargs: Any
    ) -> str:
        """Construct a LIMIT/OFFSET clause.

        Args:
            limit_value: Maximum number of rows to return
            offset_value: Number of rows to skip
            **kwargs: Additional keyword arguments (unused)

        Returns:
            Constructed LIMIT/OFFSET clause string
        """
        if limit_value is None:
            return ""

        limit_clause = f"LIMIT {limit_value}"
        if offset_value is not None:
            limit_clause += f" OFFSET {offset_value}"

        return limit_clause