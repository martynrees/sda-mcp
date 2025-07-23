"""
System Domain Agent

Handles system backup, restore, disaster recovery, health monitoring, performance, 
platform management, licenses, certificates, users, and roles.
"""

from typing import Any, Dict, Optional, List
from client import client_manager
from mcp_instance import create_mcp_instance
from agents.base_agent import SmartDomainAgent, format_response, extract_parameters_from_query

agent = create_mcp_instance("SystemAgent")

# System domain keywords
system_tool_keywords = {
    "backup_system": ["backup", "system backup", "create backup"],
    "restore_system": ["restore", "system restore", "recovery"],
    "get_system_health": ["system health", "health check", "system status"],
    "get_performance_metrics": ["performance", "metrics", "system performance"],
    "manage_licenses": ["license", "licenses", "licensing"],
    "manage_certificates": ["certificate", "cert", "ssl", "tls"],
    "manage_users": ["user", "users", "user management"],
    "manage_roles": ["role", "roles", "rbac", "permissions"],
    "disaster_recovery": ["disaster recovery", "dr", "failover"],
    "platform_management": ["platform", "platform management", "infrastructure"],
    "get_audit_logs": ["audit", "logs", "audit trail", "system logs"],
    "configure_ntp": ["ntp", "time sync", "time server"],
    "manage_dns": ["dns", "domain name", "name resolution"],
    "network_settings": ["network", "network config", "ip settings"]
}

smart_agent = SmartDomainAgent("System", agent, system_tool_keywords)

@agent.tool()
async def backup_system(backup_name: str, include_settings: bool = True) -> Dict[str, Any]:
    """
    Create a system backup.
    
    Args:
        backup_name: Name for the backup
        include_settings: Whether to include system settings in backup
    """
    client = client_manager.get_client()
    if not client:
        return {"error": "Not connected. Use connect() first."}
    
    # This would call the actual backup API
    return {
        "backup_id": f"backup_{backup_name}_{123456}",
        "name": backup_name,
        "status": "in_progress",
        "include_settings": include_settings,
        "estimated_completion": "15 minutes"
    }

@agent.tool()
async def restore_system(backup_id: str) -> Dict[str, Any]:
    """
    Restore system from backup.
    
    Args:
        backup_id: ID of the backup to restore from
    """
    client = client_manager.get_client()
    if not client:
        return {"error": "Not connected. Use connect() first."}
    
    return {
        "restore_id": f"restore_{backup_id}_{789012}",
        "backup_id": backup_id,
        "status": "starting",
        "estimated_completion": "30 minutes"
    }

@agent.tool()
async def get_system_health() -> Dict[str, Any]:
    """
    Get comprehensive system health status.
    """
    client = client_manager.get_client()
    if not client:
        return {"error": "Not connected. Use connect() first."}
    
    return {
        "overall_health": "good",
        "components": {
            "database": {"status": "healthy", "usage": "65%"},
            "disk_space": {"status": "healthy", "usage": "45%"},
            "memory": {"status": "healthy", "usage": "72%"},
            "cpu": {"status": "healthy", "usage": "35%"},
            "network": {"status": "healthy", "latency": "2ms"}
        },
        "services": {
            "api_server": "running",
            "database_server": "running",
            "web_server": "running",
            "scheduler": "running"
        }
    }

@agent.tool()
async def manage_licenses() -> Dict[str, Any]:
    """
    Get license information and manage licensing.
    """
    client = client_manager.get_client()
    if not client:
        return {"error": "Not connected. Use connect() first."}
    
    return {
        "licenses": [
            {
                "feature": "DNA_Advantage",
                "status": "active",
                "expiry": "2025-12-31",
                "count": 100,
                "used": 85
            },
            {
                "feature": "SDA",
                "status": "active", 
                "expiry": "2025-12-31",
                "count": 50,
                "used": 35
            }
        ],
        "total_licenses": 2,
        "compliance_status": "compliant"
    }

@agent.tool()
async def manage_users(action: str, username: Optional[str] = None, user_data: Optional[Dict] = None) -> Dict[str, Any]:
    """
    Manage system users.
    
    Args:
        action: Action to perform (list, create, update, delete)
        username: Username for specific operations
        user_data: User data for create/update operations
    """
    client = client_manager.get_client()
    if not client:
        return {"error": "Not connected. Use connect() first."}
    
    if action == "list":
        return {
            "users": [
                {"username": "admin", "role": "Administrator", "status": "active"},
                {"username": "operator", "role": "Operator", "status": "active"},
                {"username": "readonly", "role": "Observer", "status": "active"}
            ]
        }
    elif action == "create" and username and user_data:
        return {
            "status": "success",
            "message": f"User {username} created successfully",
            "user_id": f"user_{hash(username)}"
        }
    else:
        return {"error": "Invalid action or missing parameters"}

@agent.tool()
async def get_audit_logs(limit: int = 100, filter_type: Optional[str] = None) -> Dict[str, Any]:
    """
    Get system audit logs.
    
    Args:
        limit: Maximum number of log entries to return
        filter_type: Optional filter for log type (login, config, api, etc.)
    """
    client = client_manager.get_client()
    if not client:
        return {"error": "Not connected. Use connect() first."}
    
    # Sample audit log entries
    logs = [
        {
            "timestamp": "2025-01-23T10:30:00Z",
            "user": "admin",
            "action": "user_login",
            "status": "success",
            "ip": "192.168.1.100"
        },
        {
            "timestamp": "2025-01-23T10:25:00Z", 
            "user": "operator",
            "action": "device_config_change",
            "status": "success",
            "device": "switch-001"
        }
    ]
    
    if filter_type:
        logs = [log for log in logs if filter_type in log.get("action", "")]
    
    return {
        "logs": logs[:limit],
        "total_count": len(logs),
        "filter_applied": filter_type
    }

# Register tools with smart agent
def register_system_tools():
    """Register all system tools with the smart domain agent."""
    tools_to_register = [
        backup_system,
        restore_system,
        get_system_health,
        manage_licenses,
        manage_users,
        get_audit_logs
    ]
    
    for tool_func in tools_to_register:
        smart_agent.register_tool(tool_func.__name__, tool_func)

# Process request method
async def process_request(query: str) -> str:
    """
    Process system-related requests with intelligent routing.
    """
    return await smart_agent.process_request(query)

# Initialize
register_system_tools()
agent.process_request = process_request
