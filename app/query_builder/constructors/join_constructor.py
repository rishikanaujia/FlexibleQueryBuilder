"""JOIN clause constructor for the flexible query builder."""
from typing import Dict, List, Any

from app.query_builder.constructors.base import ClauseConstructor


class JoinConstructor(ClauseConstructor):
    """Constructor for JOIN clauses."""

    def construct(self, joins: List[Dict[str, Any]], **kwargs: Any) -> str:
        """Construct a JOIN clause.

        Args:
            joins: List of join definitions
            **kwargs: Additional keyword arguments (unused)

        Returns:
            Constructed JOIN clause string
        """
        if not joins:
            return ""

        join_statements = []

        for join_item in joins:
            join_key = join_item['key']
            join_info = join_item['info']
            use_exact = join_item.get('use_exact', False)

            if join_key == 'industry':
                # Use specific join for industry
                join_statements.append(
                    f"JOIN {self.schema}.{join_info['table']} {join_info['alias']} "
                    f"ON {join_info['alias']}.simpleIndustryId = c.simpleIndustryId"
                )
            elif join_key == 'country':
                # Use specific join for country
                join_statements.append(
                    f"JOIN {self.schema}.{join_info['table']} {join_info['alias']} "
                    f"ON {join_info['alias']}.countryId = c.countryId"
                )
            elif join_key == 'company_reverse':
                # Use reverse order company join
                join_statements.append(
                    f"JOIN {self.schema}.{join_info['table']} {join_info['alias']} "
                    f"ON {join_info['alias']}.companyId = {self.base_alias}.companyId"
                )
            elif use_exact:
                # Use the exact condition as specified
                join_statements.append(
                    f"JOIN {self.schema}.{join_info['table']} {join_info['alias']} "
                    f"ON {join_info['condition']}"
                )
            else:
                # Normal join
                join_statements.append(
                    f"JOIN {self.schema}.{join_info['table']} {join_info['alias']} "
                    f"ON {join_info['condition']}"
                )

        return " ".join(join_statements)