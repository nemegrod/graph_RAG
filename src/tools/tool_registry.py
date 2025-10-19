"""Tool registry for managing and discovering tools"""
from typing import Dict, List, Any, Callable, Optional


class ToolRegistry:
    """
    Central registry for managing tools that can be used by agents
    """
    
    def __init__(self):
        """Initialize tool registry"""
        self.tools: Dict[str, Dict[str, Any]] = {}
        self.tool_functions: Dict[str, Callable] = {}
    
    def register_tool(
        self,
        name: str,
        tool_definition: Dict[str, Any],
        tool_function: Callable
    ) -> None:
        """
        Register a tool with its definition and execution function
        
        Args:
            name: Unique tool name
            tool_definition: OpenAI function calling tool definition
            tool_function: Function to execute when tool is called
        """
        self.tools[name] = tool_definition
        self.tool_functions[name] = tool_function
    
    def unregister_tool(self, name: str) -> bool:
        """
        Unregister a tool
        
        Args:
            name: Tool name to unregister
        
        Returns:
            True if tool was unregistered, False if not found
        """
        if name in self.tools:
            del self.tools[name]
            del self.tool_functions[name]
            return True
        return False
    
    def get_tool_definition(self, name: str) -> Optional[Dict[str, Any]]:
        """
        Get tool definition by name
        
        Args:
            name: Tool name
        
        Returns:
            Tool definition or None if not found
        """
        return self.tools.get(name)
    
    def get_tool_function(self, name: str) -> Optional[Callable]:
        """
        Get tool execution function by name
        
        Args:
            name: Tool name
        
        Returns:
            Tool function or None if not found
        """
        return self.tool_functions.get(name)
    
    def get_all_tool_definitions(self) -> List[Dict[str, Any]]:
        """
        Get all registered tool definitions
        
        Returns:
            List of tool definitions
        """
        return list(self.tools.values())
    
    def get_tool_names(self) -> List[str]:
        """
        Get list of all registered tool names
        
        Returns:
            List of tool names
        """
        return list(self.tools.keys())
    
    def execute_tool(self, name: str, **kwargs) -> Any:
        """
        Execute a tool by name with given arguments
        
        Args:
            name: Tool name
            **kwargs: Tool arguments
        
        Returns:
            Tool execution result
        
        Raises:
            ValueError: If tool not found
        """
        tool_function = self.get_tool_function(name)
        if tool_function is None:
            raise ValueError(f"Tool '{name}' not found in registry")
        
        return tool_function(**kwargs)
    
    def clear(self) -> None:
        """Clear all registered tools"""
        self.tools.clear()
        self.tool_functions.clear()


# Global tool registry instance
_tool_registry: Optional[ToolRegistry] = None


def get_tool_registry() -> ToolRegistry:
    """Get or create global tool registry instance"""
    global _tool_registry
    if _tool_registry is None:
        _tool_registry = ToolRegistry()
        # Auto-register default tools
        _register_default_tools(_tool_registry)
    return _tool_registry


def _register_default_tools(registry: ToolRegistry) -> None:
    """Register default tools with the registry"""
    from src.tools.graphdb_tool import get_graphdb_tool
    
    # Register GraphDB tool
    graphdb_tool = get_graphdb_tool()
    registry.register_tool(
        name="query_jaguar_database",
        tool_definition=graphdb_tool.get_tool_definition(),
        tool_function=lambda sparql_query: graphdb_tool.execute_query_json(sparql_query)
    )

