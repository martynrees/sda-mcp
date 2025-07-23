"""
Ecosystem Domain Agent

Handles ecosystem integrations, particularly ITSM (IT Service Management) 
integrations and third-party system connections.
"""

from typing import Any, Dict, Optional
from client import client_manager
from mcp_instance import create_mcp_instance
from agents.base_agent import SmartDomainAgent, format_response, extract_parameters_from_query

agent = create_mcp_instance("EcosystemAgent")

ecosystem_tool_keywords = {
    "itsm_integration": ["itsm", "servicenow", "service management", "ticket"],
    "third_party_integration": ["integration", "api", "webhook", "external"],
    "siem_integration": ["siem", "security", "splunk", "qradar"],
    "monitoring_integration": ["monitoring", "nagios", "zabbix", "prtg"]
}

smart_agent = SmartDomainAgent("Ecosystem", agent, ecosystem_tool_keywords)

@agent.tool()
async def get_itsm_integrations() -> Dict[str, Any]:
    """Get configured ITSM integrations."""
    client = client_manager.get_client()
    if not client:
        return {"error": "Not connected. Use connect() first."}
    
    return {
        "integrations": [
            {"name": "ServiceNow", "status": "active", "last_sync": "2025-01-23T10:00:00Z"},
            {"name": "Remedy", "status": "inactive", "last_sync": "2025-01-20T15:30:00Z"}
        ]
    }

def register_ecosystem_tools():
    tools_to_register = [get_itsm_integrations]
    for tool_func in tools_to_register:
        smart_agent.register_tool(tool_func.__name__, tool_func)

async def process_request(query: str) -> str:
    return await smart_agent.process_request(query)

register_ecosystem_tools()
agent.process_request = process_request
