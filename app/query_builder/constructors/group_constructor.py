"""GROUP BY clause constructor for the flexible query builder."""
from typing import List, Any

from app.query_builder.constructors.base import ClauseConstructor


class GroupByConstructor(ClauseConstructor):
    """Constructor for GROUP BY clauses."""

    def construct(self, group_by_fields: List[str], **kwargs: Any) -> str:
        """Construct a GROUP BY clause.

        Args:
            group_by_fields: List of fields to group by
            **kwargs: Additional keyword arguments (unused)

        Returns:
            Constructed GROUP BY clause string
        """
        if not group_by_fields:
            return ""

        return f"GROUP BY {', '.join(group_by_fields)}"