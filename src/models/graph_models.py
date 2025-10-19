"""GraphDB and SPARQL-related data models"""
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field


class SPARQLBinding(BaseModel):
    """Represents a single binding in a SPARQL result"""
    variable: str = Field(..., description="Variable name")
    value: str = Field(..., description="Value")
    type: str = Field(..., description="Value type (uri, literal, bnode)")
    datatype: Optional[str] = Field(None, description="Datatype for literals")
    xml_lang: Optional[str] = Field(None, description="Language tag for literals", alias="xml:lang")
    
    class Config:
        populate_by_name = True


class SPARQLResult(BaseModel):
    """Represents a single result row from a SPARQL query"""
    bindings: Dict[str, SPARQLBinding] = Field(default_factory=dict, description="Variable bindings")
    
    def get_value(self, variable: str) -> Optional[str]:
        """Get the value of a variable"""
        return self.bindings.get(variable, {}).get("value")


class SPARQLQueryResponse(BaseModel):
    """Represents a complete SPARQL query response"""
    head: Dict[str, List[str]] = Field(..., description="Query head with variable names")
    results: Dict[str, List[Dict[str, Any]]] = Field(..., description="Query results")
    
    def get_bindings(self) -> List[Dict[str, Any]]:
        """Get all result bindings"""
        return self.results.get("bindings", [])
    
    def get_variable_names(self) -> List[str]:
        """Get list of variable names from the query"""
        return self.head.get("vars", [])
    
    def to_simple_dict(self) -> List[Dict[str, str]]:
        """
        Convert to a simplified dictionary format with just variable names and values
        
        Returns:
            List of dictionaries mapping variable names to values
        """
        simplified = []
        for binding in self.get_bindings():
            row = {}
            for var, value_obj in binding.items():
                row[var] = value_obj.get("value", "")
            simplified.append(row)
        return simplified


class GraphDBConnectionInfo(BaseModel):
    """GraphDB connection information"""
    url: str = Field(..., description="GraphDB server URL")
    repository: str = Field(..., description="Repository name")
    timeout: int = Field(default=30, description="Request timeout in seconds")
    
    @property
    def sparql_endpoint(self) -> str:
        """Get the SPARQL endpoint URL"""
        return f"{self.url}/repositories/{self.repository}"


class OntologyInfo(BaseModel):
    """Information about a loaded ontology"""
    name: str = Field(..., description="Ontology name")
    file_path: str = Field(..., description="Path to ontology file")
    namespace: str = Field(..., description="Ontology namespace")
    classes_count: Optional[int] = Field(None, description="Number of classes")
    properties_count: Optional[int] = Field(None, description="Number of properties")
    loaded_at: Optional[str] = Field(None, description="Load timestamp")

