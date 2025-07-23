"""
Authentication and Security Domain Agent

Handles all authentication, user management, certificates, and security-related operations.
"""

from typing import Any, Dict, Optional
from client import client_manager, CatalystCenterClient
from mcp_instance import create_mcp_instance
from agents.base_agent import SmartDomainAgent, format_response, extract_parameters_from_query

agent = create_mcp_instance("AuthenticationAgent")

# Authentication domain keywords
auth_tool_keywords = {
    "connect": ["connect", "connection", "login", "auth"],
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
async def connect(base_url: str, username: str, password: str) -> str:
    """Connect to Cisco Catalyst Center."""
    client = CatalystCenterClient(base_url, username, password)
    if await client.authenticate():
        client_manager.set_client(client)
        return "Successfully connected to Cisco Catalyst Center"
    return "Failed to connect to Cisco Catalyst Center"

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
        manage_certificates,
        connect
    ]
    
    for tool_func in tools_to_register:
        smart_agent.register_tool(tool_func.__name__, tool_func)

# Process request method
async def process_request(query: str) -> str:
    """
    Process authentication-related requests with intelligent routing.
    """
    return await smart_agent.process_request(query)

# Add run_tools method for router compatibility
async def run_tools(query: str) -> str:
    """Run authentication tools based on query."""
    print(f"DEBUG: Authentication run_tools called with query: {query}")
    
    # Try to extract parameters from query for connect command
    if "connect" in query.lower():
        import re
        print("DEBUG: Connect command detected")
        
        # Extract URL, username, password from query
        url_match = re.search(r'https?://[\w\.\-:]+', query)
        words = query.split()
        
        if url_match:
            base_url = url_match.group()
            print(f"DEBUG: Found URL: {base_url}")
            
            # Find username and password after the URL
            url_index = -1
            for i, word in enumerate(words):
                if base_url in word:
                    url_index = i
                    break
            
            if url_index >= 0 and len(words) > url_index + 2:
                username = words[url_index + 1]
                password = words[url_index + 2]
                print(f"DEBUG: Found credentials: {username} / {password}")
                
                # Call connect tool directly
                try:
                    print("DEBUG: Calling connect function")
                    result = await connect(base_url, username, password)
                    print(f"DEBUG: Connect result: {result}")
                    return result
                except Exception as e:
                    print(f"DEBUG: Connect error: {str(e)}")
                    return f"Connection failed: {str(e)}"
            else:
                print("DEBUG: Could not extract credentials from query")
                return "Failed to extract connection parameters from query"
        else:
            print("DEBUG: No URL found in query")
            return "No valid URL found in connection request"
    
    # Fallback to smart agent processing
    print("DEBUG: Falling back to smart agent processing")
    return await process_request(query)

# Initialize
register_auth_tools()

# Attach methods to agent
agent.process_request = process_request
agent.run_tools = run_tools
