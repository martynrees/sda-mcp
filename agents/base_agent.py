"""
Base Agent Class for Domain Agents

This provides a common interface and utility methods for all domain agents.
"""

import asyncio
import json
from typing import Any, Dict, List, Optional, Callable
from abc import ABC, abstractmethod


class BaseDomainAgent(ABC):
    """
    Base class for all domain agents providing common functionality.
    """
    
    def __init__(self, name: str, agent_instance):
        self.name = name
        self.agent = agent_instance
        self.tools_registry: Dict[str, Callable] = {}
        
    @abstractmethod
    async def process_request(self, query: str) -> str:
        """
        Process a user request and return appropriate response.
        This should be implemented by each domain agent.
        """
        pass
    
    def register_tool(self, name: str, func: Callable) -> None:
        """Register a tool function in the tools registry."""
        self.tools_registry[name] = func
    
    def get_available_tools(self) -> List[str]:
        """Get list of available tools for this domain."""
        return list(self.tools_registry.keys())
    
    async def execute_tool(self, tool_name: str, **kwargs) -> Any:
        """Execute a specific tool by name with provided arguments."""
        if tool_name not in self.tools_registry:
            return f"Error: Tool '{tool_name}' not found in {self.name} agent."
        
        try:
            tool_func = self.tools_registry[tool_name]
            if asyncio.iscoroutinefunction(tool_func):
                return await tool_func(**kwargs)
            else:
                return tool_func(**kwargs)
        except Exception as e:
            return f"Error executing tool '{tool_name}': {str(e)}"
    
    def get_tool_info(self, tool_name: str) -> Dict[str, Any]:
        """Get information about a specific tool including its signature."""
        if tool_name not in self.tools_registry:
            return {"error": f"Tool '{tool_name}' not found"}
        
        tool_func = self.tools_registry[tool_name]
        return {
            "name": tool_name,
            "doc": tool_func.__doc__ or "No documentation available",
            "is_async": asyncio.iscoroutinefunction(tool_func)
        }
    
    async def run_tools(self, query: str) -> str:
        """
        Default implementation for running tools based on query.
        Can be overridden by domain agents for more sophisticated routing.
        """
        # Simple implementation - just return available tools
        available_tools = self.get_available_tools()
        return f"Available tools in {self.name}: {', '.join(available_tools[:10])}{'...' if len(available_tools) > 10 else ''}"


class SmartDomainAgent(BaseDomainAgent):
    """
    Enhanced domain agent with query analysis and smart tool selection.
    """
    
    def __init__(self, name: str, agent_instance, tool_keywords: Optional[Dict[str, List[str]]] = None):
        super().__init__(name, agent_instance)
        self.tool_keywords = tool_keywords or {}
    
    def analyze_query(self, query: str) -> List[str]:
        """
        Analyze query and suggest relevant tools based on keywords.
        """
        query_lower = query.lower()
        relevant_tools = []
        
        for tool_name, keywords in self.tool_keywords.items():
            if tool_name in self.tools_registry:
                for keyword in keywords:
                    if keyword.lower() in query_lower:
                        relevant_tools.append(tool_name)
                        break
        
        return relevant_tools
    
    async def process_request(self, query: str) -> str:
        """
        Process request with smart tool selection.
        """
        relevant_tools = self.analyze_query(query)
        
        if not relevant_tools:
            return await self.run_tools(query)
        
        # For now, return information about relevant tools
        # In a more sophisticated implementation, you could automatically execute tools
        tool_info = []
        for tool_name in relevant_tools[:5]:  # Limit to top 5 tools
            info = self.get_tool_info(tool_name)
            tool_info.append(f"- {tool_name}: {info.get('doc', 'No description')[:100]}...")
        
        return f"Based on your query '{query}', here are the most relevant tools in {self.name}:\n\n" + "\n".join(tool_info)


# Utility functions for domain agents

def extract_parameters_from_query(query: str, expected_params: List[str]) -> Dict[str, Any]:
    """
    Extract parameters from a natural language query.
    This is a simple implementation - can be enhanced with NLP.
    """
    parameters = {}
    query_lower = query.lower()
    
    # Simple pattern matching for common parameters
    import re
    
    # Extract IP addresses
    ip_pattern = r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b'
    ips = re.findall(ip_pattern, query)
    if ips and 'ip' in expected_params:
        parameters['ip'] = ips[0]
    
    # Extract device names (simple heuristic)
    device_pattern = r'\b(?:device|switch|router)\s+([a-zA-Z0-9\-_.]+)\b'
    devices = re.findall(device_pattern, query_lower)
    if devices and 'hostname' in expected_params:
        parameters['hostname'] = devices[0]
    
    # Extract site names
    site_pattern = r'\bsite\s+([a-zA-Z0-9\-_.]+)\b'
    sites = re.findall(site_pattern, query_lower)
    if sites and 'site' in expected_params:
        parameters['site'] = sites[0]
    
    return parameters


def format_response(data: Any, format_type: str = "summary") -> str:
    """
    Format API response data in a user-friendly way.
    """
    if isinstance(data, dict):
        if "error" in data:
            return f"❌ Error: {data['error']}"
        
        if format_type == "summary":
            # Create a brief summary
            summary_items = []
            for key, value in data.items():
                if isinstance(value, (str, int, float, bool)):
                    summary_items.append(f"{key}: {value}")
                elif isinstance(value, list):
                    summary_items.append(f"{key}: {len(value)} items")
                elif isinstance(value, dict):
                    summary_items.append(f"{key}: {type(value).__name__}")
            
            return "📊 " + " | ".join(summary_items[:5])
        
        elif format_type == "detailed":
            return f"📄 Response:\n```json\n{json.dumps(data, indent=2)}\n```"
    
    elif isinstance(data, list):
        return f"📋 Found {len(data)} items"
    
    elif isinstance(data, str):
        return f"📝 {data}"
    
    return f"✅ Operation completed: {type(data).__name__}"
