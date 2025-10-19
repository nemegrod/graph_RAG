"""GraphDB connection and query service"""
import os
import requests
from urllib.parse import urlencode
from typing import Optional, Dict, Any
from dotenv import load_dotenv
from src.models.graph_models import GraphDBConnectionInfo, SPARQLQueryResponse

# Load environment variables
load_dotenv()


class GraphDBService:
    """Service for managing GraphDB connections and queries"""
    
    def __init__(
        self,
        url: Optional[str] = None,
        repository: Optional[str] = None,
        timeout: int = 30
    ):
        """
        Initialize GraphDB service
        
        Args:
            url: GraphDB server URL (defaults to env var GRAPHDB_URL)
            repository: Repository name (defaults to env var GRAPHDB_REPOSITORY)
            timeout: Request timeout in seconds
        """
        self.connection_info = GraphDBConnectionInfo(
            url=url or os.getenv("GRAPHDB_URL", "http://localhost:7200"),
            repository=repository or os.getenv("GRAPHDB_REPOSITORY", "Jaguars"),
            timeout=timeout
        )
    
    def execute_sparql_query(
        self,
        query: str,
        accept_format: str = "application/sparql-results+json"
    ) -> Dict[str, Any]:
        """
        Execute a SPARQL query against GraphDB
        
        Args:
            query: SPARQL query string
            accept_format: Accept header format
        
        Returns:
            Query results as dictionary
        
        Raises:
            ConnectionError: If unable to connect to GraphDB
            requests.HTTPError: If HTTP error occurs
            Exception: For other errors
        """
        try:
            params = {'query': query.strip()}
            headers = {
                'Accept': accept_format,
                'Content-Type': 'application/x-www-form-urlencoded'
            }
            
            response = requests.post(
                self.connection_info.sparql_endpoint,
                data=urlencode(params),
                headers=headers,
                timeout=self.connection_info.timeout
            )
            
            response.raise_for_status()
            result_data = response.json()
            
            return result_data
            
        except requests.exceptions.ConnectionError as e:
            error_msg = f"Could not connect to GraphDB at {self.connection_info.url}"
            raise ConnectionError(error_msg) from e
        
        except requests.exceptions.HTTPError:
            raise
        
        except Exception as e:
            raise Exception(f"Unexpected error executing SPARQL query: {e}") from e
    
    def execute_sparql_query_parsed(self, query: str) -> SPARQLQueryResponse:
        """
        Execute a SPARQL query and return parsed response
        
        Args:
            query: SPARQL query string
        
        Returns:
            Parsed SPARQL query response
        """
        result = self.execute_sparql_query(query)
        return SPARQLQueryResponse(**result)
    
    def test_connection(self) -> bool:
        """
        Test connection to GraphDB
        
        Returns:
            True if connection successful, False otherwise
        """
        try:
            # Simple query to test connection
            test_query = "SELECT * WHERE { ?s ?p ?o } LIMIT 1"
            self.execute_sparql_query(test_query)
            return True
        except Exception:
            return False
    
    def get_repository_info(self) -> Dict[str, Any]:
        """
        Get information about the repository
        
        Returns:
            Repository information dictionary
        """
        try:
            url = f"{self.connection_info.url}/repositories/{self.connection_info.repository}"
            response = requests.get(url, timeout=self.connection_info.timeout)
            response.raise_for_status()
            return response.json()
        except Exception:
            return {}
    
    @property
    def sparql_endpoint(self) -> str:
        """Get the SPARQL endpoint URL"""
        return self.connection_info.sparql_endpoint


# Global GraphDB service instance
_graphdb_service: Optional[GraphDBService] = None


def get_graphdb_service() -> GraphDBService:
    """Get or create global GraphDB service instance"""
    global _graphdb_service
    if _graphdb_service is None:
        _graphdb_service = GraphDBService()
    return _graphdb_service

