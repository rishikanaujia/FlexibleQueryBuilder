"""Join analyzer for the flexible query builder."""
from typing import Dict, List, Set, Tuple, Any

from app.utils.constants import JOIN_PATHS


class JoinAnalyzer:
    """Analyzer for determining required joins based on field usage."""

    def __init__(self):
        """Initialize the join analyzer."""
        pass

    def determine_joins(self, field_dependencies: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Determine required joins based on field dependencies.

        Args:
            field_dependencies: Field dependency information

        Returns:
            List of required joins
        """
        # Extract data from field dependencies
        used_aliases = field_dependencies['used_aliases']
        query_params = field_dependencies['query_params']

        # Track joins to be added
        joins = []

        # Map aliases to potential joins
        for alias in used_aliases:
            matching_joins = self._find_joins_for_alias(alias)

            if not matching_joins:
                continue

            # Handle parameter-specific joins
            self._handle_specific_joins(alias, matching_joins, query_params, joins)

            # If no specific handling, add the first matching join
            if not self._has_join_for_alias(alias, joins) and matching_joins:
                self._add_join(matching_joins[0][0], matching_joins[0][1], joins)

        # Order joins to ensure dependencies are met
        return self._order_joins(joins)

    def _find_joins_for_alias(self, alias: str) -> List[Tuple[str, Dict]]:
        """Find all joins that provide a given alias."""
        matching_joins = []
        for join_key, join_info in JOIN_PATHS.items():
            if join_info['alias'] == alias:
                matching_joins.append((join_key, join_info))
        return matching_joins

    def _has_join_for_alias(self, alias: str, joins: List[Dict[str, Any]]) -> bool:
        """Check if we already have a join that provides this alias."""
        for join in joins:
            if join['info']['alias'] == alias:
                return True
        return False

    def _handle_specific_joins(
            self,
            alias: str,
            matching_joins: List[Tuple[str, Dict]],
            query_params: Dict[str, str],
            joins: List[Dict[str, Any]]
    ) -> None:
        """Handle parameter-specific joins."""
        for field, value in query_params.items():
            if field == 'tr.transactionIdTypeId':
                if value == '1':
                    # Use tt for transaction type in this case
                    for join_key, join_info in matching_joins:
                        if join_key == 'type':
                            self._add_join(join_key, join_info, joins)
                elif value == '14':
                    # Use trtype for transaction type in this case
                    for join_key, join_info in matching_joins:
                        if join_key == 'transaction_type':
                            self._add_join(join_key, join_info, joins)
            elif field.startswith('c.'):
                # Company-related joins
                if alias == 'c':
                    for join_key, join_info in matching_joins:
                        if join_key == 'company':
                            self._add_join(join_key, join_info, joins)
            elif field.startswith('si.'):
                # Industry-related joins
                if alias == 'si':
                    for join_key, join_info in matching_joins:
                        if join_key == 'industry':
                            self._add_join(join_key, join_info, joins)
                            # Also need company join for industry
                            self._add_dependent_join('company', joins)
            elif field.startswith('geo.'):
                # Country-related joins
                if alias == 'geo':
                    for join_key, join_info in matching_joins:
                        if join_key == 'country':
                            self._add_join(join_key, join_info, joins)
                            # Also need company join for country
                            self._add_dependent_join('company', joins)

    def _add_dependent_join(self, join_key: str, joins: List[Dict[str, Any]]) -> None:
        """Add a dependent join if not already added."""
        if join_key not in [j['key'] for j in joins]:
            join_info = JOIN_PATHS.get(join_key)
            if join_info:
                self._add_join(join_key, join_info, joins)

    def _add_join(
            self,
            join_key: str,
            join_info: Dict[str, Any],
            joins: List[Dict[str, Any]]
    ) -> None:
        """Add a join if not already added."""
        if join_key not in [j['key'] for j in joins]:
            # Check if we need special handling for this join
            if join_key == 'company_reverse':
                # For company_reverse, we want to use the exact condition
                joins.append({
                    'key': join_key,
                    'info': join_info,
                    'use_exact': True
                })
            else:
                joins.append({
                    'key': join_key,
                    'info': join_info,
                    'use_exact': False
                })

    def _order_joins(self, joins: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Order joins to ensure dependencies are met."""
        ordered_joins = []
        remaining_joins = joins.copy()

        # First add company joins
        company_joins = [j for j in remaining_joins if j['info']['table'] == 'ciqCompany']
        for join in company_joins:
            ordered_joins.append(join)
            remaining_joins.remove(join)

        # Next add transaction type joins
        tt_joins = [j for j in remaining_joins if j['info']['table'] == 'ciqTransactionType']
        for join in tt_joins:
            ordered_joins.append(join)
            remaining_joins.remove(join)

        # Add remaining joins
        for join in remaining_joins:
            ordered_joins.append(join)

        return ordered_joins