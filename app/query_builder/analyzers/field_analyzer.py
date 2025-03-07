"""Field usage analyzer for the flexible query builder."""
import re
from typing import Dict, List, Set, Any


class FieldAnalyzer:
    """Analyzer for determining field usage in queries."""

    def __init__(self):
        """Initialize the field analyzer."""
        pass

    def analyze_fields(
            self,
            select_fields: List[str],
            where_conditions: List[str],
            group_by_fields: List[str],
            order_by_clauses: List[str]
    ) -> Dict[str, Any]:
        """Analyze field usage to determine dependencies.

        Args:
            select_fields: List of selected fields
            where_conditions: List of where conditions
            group_by_fields: List of group by fields
            order_by_clauses: List of order by clauses

        Returns:
            Dictionary with field dependency information
        """
        # Find all aliases used in the query
        used_aliases = self._find_all_field_aliases(
            select_fields, where_conditions, group_by_fields, order_by_clauses
        )

        # Extract field references
        field_refs = self._extract_field_references(
            select_fields, where_conditions, group_by_fields, order_by_clauses
        )

        # Extract parameter values from where conditions
        query_params = self._extract_query_params(where_conditions)

        return {
            'used_aliases': used_aliases,
            'field_refs': field_refs,
            'query_params': query_params
        }

    def _find_all_field_aliases(
            self,
            select_fields: List[str],
            where_conditions: List[str],
            group_by_fields: List[str],
            order_by_clauses: List[str]
    ) -> Set[str]:
        """Find all field aliases used in the query."""
        # Compile all text that might contain field references
        all_text = ' '.join(
            select_fields +
            where_conditions +
            group_by_fields +
            order_by_clauses
        )

        # Extract all field references like 'c.companyName'
        field_refs = re.findall(r'([a-z]+)\.([a-zA-Z_]+)', all_text)

        # Collect unique aliases
        aliases = set()
        for alias, field in field_refs:
            aliases.add(alias)

        return aliases

    def _extract_field_references(
            self,
            select_fields: List[str],
            where_conditions: List[str],
            group_by_fields: List[str],
            order_by_clauses: List[str]
    ) -> Dict[str, Set[str]]:
        """Extract field references used in the query."""
        # Compile all text that might contain field references
        all_text = ' '.join(
            select_fields +
            where_conditions +
            group_by_fields +
            order_by_clauses
        )

        # Extract all field references like 'c.companyName'
        field_refs = re.findall(r'([a-z]+)\.([a-zA-Z_]+)', all_text)

        # Organize by alias
        refs_by_alias = {}
        for alias, field in field_refs:
            if alias not in refs_by_alias:
                refs_by_alias[alias] = set()
            refs_by_alias[alias].add(field)

        return refs_by_alias

    def _extract_query_params(self, where_conditions: List[str]) -> Dict[str, str]:
        """Extract query parameters from where conditions."""
        params = {}
        for condition in where_conditions:
            # Parse conditions like "tr.transactionIdTypeId = '1'"
            match = re.match(r'([a-z]+\.[a-zA-Z_]+)\s*=\s*\'([^\']+)\'', condition)
            if match:
                field, value = match.groups()
                params[field] = value

            # Parse IN conditions like "si.simpleIndustryId IN ('32', '34')"
            match = re.match(r'([a-z]+\.[a-zA-Z_]+)\s+IN\s+\(([^\)]+)\)', condition)
            if match:
                field, values_str = match.groups()
                values = [v.strip().strip("'") for v in values_str.split(',')]
                params[field] = ','.join(values)

        return params