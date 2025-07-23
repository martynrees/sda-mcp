"""
Appliance Domain Agent

Handles Cisco IMC appliance management and hardware operations.
"""

from typing import Any, Dict, Optional
from client import client_manager
from mcp_instance import create_mcp_instance
from agents.base_agent import SmartDomainAgent, format_response, extract_parameters_from_query

agent = create_mcp_instance("ApplianceAgent")

# Appliance domain keywords
appliance_tool_keywords = {
    "get_imc_status": ["imc", "appliance status", "hardware status"],
    "configure_imc": ["configure imc", "imc config", "appliance config"],
    "get_hardware_health": ["hardware health", "server health", "appliance health"],
    "manage_server_power": ["power", "power management", "server power"],
    "get_system_info": ["system info", "hardware info", "appliance info"],
    "configure_bios": ["bios", "bios settings", "firmware"],
    "manage_storage": ["storage", "disk", "raid", "storage management"],
    "network_adapter_config": ["network adapter", "nic", "network interface"]
}

smart_agent = SmartDomainAgent("Appliance", agent, appliance_tool_keywords)

@agent.tool()
async def get_imc_status() -> Dict[str, Any]:
    """
    Get the status of Cisco IMC appliances.
    """
    client = client_manager.get_client()
    if not client:
        return {"error": "Not connected. Use connect() first."}
    
    # Placeholder implementation - replace with actual IMC API calls
    return {
        "status": "operational",
        "appliances": [
            {"id": "imc-001", "status": "online", "health": "good"},
            {"id": "imc-002", "status": "online", "health": "warning"}
        ]
    }

@agent.tool()
async def get_hardware_health() -> Dict[str, Any]:
    """
    Get hardware health status for appliances.
    """
    client = client_manager.get_client()
    if not client:
        return {"error": "Not connected. Use connect() first."}
    
    return {
        "overall_health": "good",
        "components": {
            "cpu": "normal",
            "memory": "normal",
            "storage": "warning",
            "network": "normal",
            "temperature": "normal"
        }
    }

@agent.tool()
async def manage_server_power(action: str, server_id: Optional[str] = None) -> Dict[str, Any]:
    """
    Manage server power operations.
    
    Args:
        action: Power action (on, off, restart, status)
        server_id: Optional server ID to target specific server
    """
    client = client_manager.get_client()
    if not client:
        return {"error": "Not connected. Use connect() first."}
    
    valid_actions = ["on", "off", "restart", "status"]
    if action not in valid_actions:
        return {"error": f"Invalid action. Valid actions: {valid_actions}"}
    
    return {
        "action": action,
        "server_id": server_id or "all",
        "status": "success",
        "message": f"Power {action} operation completed"
    }

# Register tools with smart agent
def register_appliance_tools():
    """Register all appliance tools with the smart domain agent."""
    tools_to_register = [
        get_imc_status,
        get_hardware_health,
        manage_server_power
    ]
    
    for tool_func in tools_to_register:
        smart_agent.register_tool(tool_func.__name__, tool_func)

# Process request method
async def process_request(query: str) -> str:
    """
    Process appliance-related requests with intelligent routing.
    """
    return await smart_agent.process_request(query)

# Initialize
register_appliance_tools()
agent.process_request = process_request
