"""SQL query constructor for the flexible query builder."""
from typing import Dict, List, Optional, Any

from app.query_builder.constructors.base import ClauseConstructor
from app.query_builder.constructors.select_constructor import SelectConstructor
from app.query_builder.constructors.from_constructor import FromConstructor
from app.query_builder.constructors.join_constructor import JoinConstructor
from app.query_builder.constructors.where_constructor import WhereConstructor
from app.query_builder.constructors.group_constructor import GroupByConstructor
from app.query_builder.constructors.order_constructor import OrderByConstructor
from app.query_builder.constructors.limit_constructor import LimitOffsetConstructor


class SQLQueryConstructor:
    """Constructor for complete SQL queries."""

    def __init__(self, schema: str, base_table: str, base_alias: str):
        """Initialize the SQL query constructor.

        Args:
            schema: Database schema name
            base_table: Base table name
            base_alias: Base table alias
        """
        self.schema = schema
        self.base_table = base_table
        self.base_alias = base_alias

        # Create clause constructors
        self.select_constructor = SelectConstructor(schema, base_table, base_alias)
        self.from_constructor = FromConstructor(schema, base_table, base_alias)
        self.join_constructor = JoinConstructor(schema, base_table, base_alias)
        self.where_constructor = WhereConstructor(schema, base_table, base_alias)
        self.group_constructor = GroupByConstructor(schema, base_table, base_alias)
        self.order_constructor = OrderByConstructor(schema, base_table, base_alias)
        self.limit_constructor = LimitOffsetConstructor(schema, base_table, base_alias)

    def build_query(
            self,
            select_fields: List[str],
            where_conditions: List[str],
            group_by_fields: List[str],
            order_by_clauses: List[str],
            limit_value: Optional[int],
            offset_value: Optional[int],
            joins: List[Dict[str, Any]]
    ) -> str:
        """Build the complete SQL query.

        Args:
            select_fields: List of selected fields
            where_conditions: List of where conditions
            group_by_fields: List of group by fields
            order_by_clauses: List of order by clauses
            limit_value: Limit value
            offset_value: Offset value
            joins: List of required joins

        Returns:
            Complete SQL query string
        """
        # Build each clause
        select_clause = self.select_constructor.construct(select_fields=select_fields)
        from_clause = self.from_constructor.construct()
        join_clause = self.join_constructor.construct(joins=joins)
        where_clause = self.where_constructor.construct(where_conditions=where_conditions)
        group_by_clause = self.group_constructor.construct(group_by_fields=group_by_fields)
        order_by_clause = self.order_constructor.construct(order_by_clauses=order_by_clauses)
        limit_clause = self.limit_constructor.construct(
            limit_value=limit_value,
            offset_value=offset_value
        )

        # Combine all clauses
        query_parts = [select_clause, from_clause]

        if join_clause:
            query_parts.append(join_clause)
        if where_clause:
            query_parts.append(where_clause)
        if group_by_clause:
            query_parts.append(group_by_clause)
        if order_by_clause:
            query_parts.append(order_by_clause)
        if limit_clause:
            query_parts.append(limit_clause)

        return " ".join(query_parts)