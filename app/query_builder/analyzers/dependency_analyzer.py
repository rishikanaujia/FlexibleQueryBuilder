"""Join dependency analyzer for the flexible query builder."""
from typing import Dict, List, Set, Any

from app.utils.constants import JOIN_PATHS


class DependencyAnalyzer:
    """Analyzer for determining join dependencies."""

    def __init__(self):
        """Initialize the dependency analyzer."""
        # Define known join dependencies
        self.join_dependencies = {
            'industry': ['company'],  # industry join requires company join
            'country': ['company'],  # country join requires company join
        }

    def analyze_join_dependencies(self, joins: List[Dict[str, Any]]) -> Set[str]:
        """Analyze joins to determine additional required joins.

        Args:
            joins: List of joins already determined

        Returns:
            Set of additional join keys required
        """
        required_joins = set()
        existing_join_keys = {j['key'] for j in joins}

        # Check each join for dependencies
        for join in joins:
            join_key = join['key']

            # If this join has dependencies
            if join_key in self.join_dependencies:
                # Add each dependency if not already in the join list
                for dep_key in self.join_dependencies[join_key]:
                    if dep_key not in existing_join_keys:
                        required_joins.add(dep_key)

        return required_joins