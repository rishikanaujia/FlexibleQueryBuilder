"""Main flexible SQL query builder class."""
import logging
from typing import Dict, List, Optional

from app.query_builder.parsers import RequestParserFactory
from app.query_builder.analyzers import FieldAnalyzer, JoinAnalyzer
from app.utils.errors import QueryBuildError

# Setup logging
logger = logging.getLogger(__name__)


class FlexibleQueryBuilder:
    """Dynamic SQL query builder that supports flexible parameters."""

    def __init__(self, schema: str, base_table: str = "ciqTransaction", base_alias: str = "tr"):
        """Initialize the query builder with schema and base table information."""
        self.schema = schema
        self.base_table = base_table
        self.base_alias = base_alias

        # Query components
        self.select_fields = []
        self.where_conditions = []
        self.group_by_fields = []
        self.order_by_clauses = []
        self.limit_value = None
        self.offset_value = None
        self.joins = []

        # Create helper objects
        self.parser_factory = RequestParserFactory()
        self.field_analyzer = FieldAnalyzer()
        self.join_analyzer = JoinAnalyzer()

    def parse_request_params(self, params: Dict[str, str]) -> None:
        """Parse request parameters into SQL query components."""
        try:
            # Process each parameter using appropriate parser
            for key, value in params.items():
                parser = self.parser_factory.get_parser(key)
                if parser:
                    parser.parse(key, value, self)

            # If no select fields specified, use * as default
            if not self.select_fields:
                self.select_fields = [f"{self.base_alias}.*"]

            # Analyze fields to determine required joins
            field_dependencies = self.field_analyzer.analyze_fields(
                self.select_fields,
                self.where_conditions,
                self.group_by_fields,
                self.order_by_clauses
            )

            # Determine required joins based on field dependencies
            self.joins = self.join_analyzer.determine_joins(field_dependencies)

        except ValueError as e:
            # Handle numeric conversion errors
            raise QueryBuildError(f"Invalid numeric value: {str(e)}")
        except Exception as e:
            # Handle other parsing errors
            logger.error(f"Error parsing parameters: {e}", exc_info=True)
            raise QueryBuildError(f"Error parsing query parameters: {str(e)}")

    def build_query(self) -> str:
        """Build the complete SQL query."""
        # This will be replaced with calls to constructor modules later
        pass