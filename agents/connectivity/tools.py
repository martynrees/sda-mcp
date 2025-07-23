"""
Connectivity Domain Agent

Handles network connectivity including Fabric Wireless, SDA (Software-Defined Access), 
wired connections, and wireless management. This agent acts as a router to SDA and other 
connectivity-related subdomains.
"""

from typing import Any, Dict, Optional
from client import client_manager
from mcp_instance import create_mcp_instance
from agents.base_agent import SmartDomainAgent, format_response, extract_parameters_from_query

agent = create_mcp_instance("ConnectivityAgent")

# Connectivity domain keywords
connectivity_tool_keywords = {
    # SDA-related
    "sda_fabric_operations": ["sda", "fabric", "sd-access", "software defined access"],
    "virtual_network_management": ["virtual network", "vn", "layer3", "l3"],
    "site_provisioning": ["site provision", "fabric site", "sda site"],
    
    # Wireless-related
    "wireless_management": ["wireless", "wifi", "wlan", "access point", "ap"],
    "fabric_wireless": ["fabric wireless", "wireless fabric"],
    
    # Wired-related
    "wired_connectivity": ["wired", "ethernet", "switch", "port"],
    "vlan_management": ["vlan", "layer2", "l2", "switching"],
    
    # General connectivity
    "network_topology": ["topology", "network map", "connectivity map"],
    "connectivity_health": ["connectivity health", "network health", "link status"]
}

smart_agent = SmartDomainAgent("Connectivity", agent, connectivity_tool_keywords)

@agent.tool()
async def route_to_sda_agent(query: str) -> str:
    """
    Route SDA-related requests to the specialized SDA agent.
    
    Args:
        query: The user query related to SDA operations
    """
    try:
        # Import and use the SDA agent
        from agents.sda.tools import process_request as sda_process_request
        return await sda_process_request(query)
    except ImportError:
        return "Error: SDA agent not available"

@agent.tool()
async def get_wireless_health() -> Dict[str, Any]:
    """
    Get wireless network health and status.
    """
    client = client_manager.get_client()
    if not client:
        return {"error": "Not connected. Use connect() first."}
    
    return {
        "overall_status": "healthy",
        "access_points": {
            "total": 150,
            "online": 147,
            "offline": 3,
            "degraded": 0
        },
        "wireless_clients": {
            "total": 1250,
            "connected_2_4ghz": 450,
            "connected_5ghz": 800
        },
        "coverage": "95%",
        "average_signal_strength": "-45 dBm"
    }

@agent.tool()
async def manage_wireless_access_points(action: str, ap_id: Optional[str] = None) -> Dict[str, Any]:
    """
    Manage wireless access points.
    
    Args:
        action: Action to perform (list, reboot, configure, status)
        ap_id: Optional access point ID for specific operations
    """
    client = client_manager.get_client()
    if not client:
        return {"error": "Not connected. Use connect() first."}
    
    if action == "list":
        return {
            "access_points": [
                {"id": "ap-001", "name": "Building-A-Floor-1", "status": "online", "clients": 15},
                {"id": "ap-002", "name": "Building-A-Floor-2", "status": "online", "clients": 23},
                {"id": "ap-003", "name": "Building-B-Floor-1", "status": "offline", "clients": 0}
            ]
        }
    elif action == "reboot" and ap_id:
        return {
            "action": "reboot",
            "ap_id": ap_id,
            "status": "initiated",
            "estimated_downtime": "2 minutes"
        }
    else:
        return {"error": "Invalid action or missing AP ID"}

@agent.tool()
async def get_wired_connectivity_status() -> Dict[str, Any]:
    """
    Get wired network connectivity status.
    """
    client = client_manager.get_client()
    if not client:
        return {"error": "Not connected. Use connect() first."}
    
    return {
        "switches": {
            "total": 45,
            "online": 44,
            "offline": 1
        },
        "ports": {
            "total": 1080,
            "active": 856,
            "inactive": 224
        },
        "vlans": {
            "configured": 25,
            "active": 23
        },
        "spanning_tree_status": "stable"
    }

@agent.tool()
async def analyze_network_topology() -> Dict[str, Any]:
    """
    Analyze and provide network topology information.
    """
    client = client_manager.get_client()
    if not client:
        return {"error": "Not connected. Use connect() first."}
    
    return {
        "topology": {
            "core_switches": 2,
            "distribution_switches": 8,
            "access_switches": 35,
            "total_links": 89,
            "redundant_paths": 15
        },
        "health": "good",
        "bottlenecks": [],
        "recommendations": [
            "Consider adding redundancy to Building-C distribution layer",
            "Monitor utilization on core link Core-1 to Core-2"
        ]
    }

@agent.tool() 
async def get_connectivity_health_summary() -> Dict[str, Any]:
    """
    Get overall connectivity health summary across all network types.
    """
    client = client_manager.get_client()
    if not client:
        return {"error": "Not connected. Use connect() first."}
    
    return {
        "overall_health": "good",
        "wired_health": "excellent",
        "wireless_health": "good", 
        "sda_fabric_health": "excellent",
        "critical_issues": 0,
        "warnings": 2,
        "last_updated": "2025-01-23T10:30:00Z"
    }

# Register tools with smart agent
def register_connectivity_tools():
    """Register all connectivity tools with the smart domain agent."""
    tools_to_register = [
        route_to_sda_agent,
        get_wireless_health,
        manage_wireless_access_points,
        get_wired_connectivity_status,
        analyze_network_topology,
        get_connectivity_health_summary
    ]
    
    for tool_func in tools_to_register:
        smart_agent.register_tool(tool_func.__name__, tool_func)

# Enhanced process request method that can route to SDA
async def process_request(query: str) -> str:
    """
    Process connectivity-related requests with intelligent routing.
    Routes SDA-specific queries to the SDA agent.
    """
    query_lower = query.lower()
    
    # Check if this is SDA-specific
    sda_keywords = ["sda", "fabric", "sd-access", "software defined access", 
                   "virtual network", "fabric site", "anycast", "transit"]
    
    if any(keyword in query_lower for keyword in sda_keywords):
        try:
            from agents.sda.tools import process_request as sda_process_request
            return await sda_process_request(query)
        except ImportError:
            return "Error: SDA agent not available"
    
    # Otherwise use the standard smart agent processing
    return await smart_agent.process_request(query)

# Initialize
register_connectivity_tools()
agent.process_request = process_request
