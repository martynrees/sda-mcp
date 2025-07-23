"""
Authentication and Security Domain Agent

Handles all authentication, user management, certificates, and security-related operations.
"""

from typing import Any, Dict, Optional
from client import client_manager
from mcp_instance import create_mcp_instance
from agents.base_agent import SmartDomainAgent, format_response, extract_parameters_from_query

agent = create_mcp_instance("AuthenticationAgent")

# Authentication domain keywords
auth_tool_keywords = {
    "authenticate_user": ["authenticate", "login", "sign in", "auth"],
    "manage_certificates": ["certificate", "cert", "ssl", "tls", "pki"],
    "manage_users": ["user", "users", "account", "accounts"],
    "manage_roles": ["role", "roles", "permission", "permissions", "rbac"],
    "get_auth_status": ["auth status", "authentication status", "login status"],
    "configure_ldap": ["ldap", "active directory", "ad", "directory service"],
    "manage_tokens": ["token", "tokens", "api key", "api keys"],
    "security_policies": ["security policy", "password policy", "access policy"]
}

smart_agent = SmartDomainAgent("Authentication", agent, auth_tool_keywords)

@agent.tool()
async def authenticate_user(username: str, password: str, domain: Optional[str] = None) -> Dict[str, Any]:
    """
    Authenticate a user with Catalyst Center.
    
    Args:
        username: Username for authentication
        password: Password for authentication
        domain: Optional domain for authentication
    """
    client = client_manager.get_client()
    if not client:
        return {"error": "Not connected. Use connect() first."}
    
    # This would typically call the actual authentication API
    # For now, return a placeholder response
    return {
        "status": "success",
        "message": f"User {username} authenticated successfully",
        "domain": domain or "local"
    }

@agent.tool()
async def get_user_roles(username: str) -> Dict[str, Any]:
    """
    Get roles and permissions for a specific user.
    
    Args:
        username: Username to query roles for
    """
    client = client_manager.get_client()
    if not client:
        return {"error": "Not connected. Use connect() first."}
    
    # Placeholder implementation
    return {
        "username": username,
        "roles": ["network_admin", "device_manager"],
        "permissions": ["read", "write", "execute"]
    }

@agent.tool()
async def manage_certificates() -> Dict[str, Any]:
    """
    Manage SSL/TLS certificates in the system.
    """
    client = client_manager.get_client()
    if not client:
        return {"error": "Not connected. Use connect() first."}
    
    # Placeholder implementation
    return {
        "certificates": [
            {"name": "system_cert", "status": "valid", "expiry": "2025-12-31"},
            {"name": "api_cert", "status": "valid", "expiry": "2025-06-30"}
        ]
    }

# Register tools with smart agent
def register_auth_tools():
    """Register all authentication tools with the smart domain agent."""
    tools_to_register = [
        authenticate_user,
        get_user_roles,
        manage_certificates
    ]
    
    for tool_func in tools_to_register:
        smart_agent.register_tool(tool_func.__name__, tool_func)

# Process request method
async def process_request(query: str) -> str:
    """
    Process authentication-related requests with intelligent routing.
    """
    return await smart_agent.process_request(query)

# Initialize
register_auth_tools()
agent.process_request = process_request
