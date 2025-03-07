"""SELECT clause constructor for the flexible query builder."""
from typing import List, Any

from app.query_builder.constructors.base import ClauseConstructor


class SelectConstructor(ClauseConstructor):
    """Constructor for SELECT clauses."""

    def construct(self, select_fields: List[str], **kwargs: Any) -> str:
        """Construct a SELECT clause.

        Args:
            select_fields: List of fields to select
            **kwargs: Additional keyword arguments (unused)

        Returns:
            Constructed SELECT clause string
        """
        if not select_fields:
            # Default to selecting all columns from base table
            return f"SELECT {self.base_alias}.*"

        return f"SELECT {', '.join(select_fields)}"