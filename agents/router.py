import importlib
import re
from typing import Dict, Optional, Any

from mcp_instance import create_mcp_instance

# Create the main router agent
router_agent = create_mcp_instance("RouterAgent")

# In-memory cache for loaded domain agents
domain_agents = {}

# Domain routing keywords for intelligent prompt routing
DOMAIN_KEYWORDS = {
    "authentication": ["auth", "authentication", "login", "token", "credential", "user", "password", "certificate", "connect", "connection"],
    "appliance": ["imc", "appliance", "cisco imc", "hardware", "server"],
    "system": ["backup", "restore", "health", "performance", "platform", "license", "certificate", "user", "role", "disaster recovery"],
    "connectivity": ["fabric", "wireless", "wired", "sda", "sd-access", "connectivity"],
    "ecosystem": ["itsm", "integration", "ecosystem"],
    "events": ["event", "events", "notification", "alert"],
    "network_inventory": ["device", "inventory", "client", "application", "compliance", "eox", "sensor", "site", "topology", "security", "advisory"],
    "operational_tasks": ["command", "discovery", "file", "path", "trace", "report", "tag", "task", "operation"],
    "policy": ["policy", "endpoint", "analytics", "application policy"],
    "site_management": ["configuration", "template", "onboarding", "pnp", "replacement", "automation", "lan automation", "network settings", "site design", "swim", "software image"],
    "system_settings": ["setting", "settings", "configuration", "system config"],
    "assurance": ["assurance", "monitoring", "analytics", "health", "performance", "issue", "problem"]
}

def classify_query(query: str) -> str:
    """
    Classify user query to determine the appropriate domain.
    Returns the domain name that best matches the query.
    """
    query_lower = query.lower()
    
    # Score each domain based on keyword matches
    domain_scores = {}
    
    for domain, keywords in DOMAIN_KEYWORDS.items():
        score = 0
        for keyword in keywords:
            if keyword in query_lower:
                # Give higher weight to exact matches
                if re.search(r'\b' + re.escape(keyword) + r'\b', query_lower):
                    score += 2
                else:
                    score += 1
        domain_scores[domain] = score
      # Special routing logic for common patterns
    if any(term in query_lower for term in ["connect", "login", "auth", "authenticate"]):
        return "authentication"  # Route connect requests to authentication
    elif any(term in query_lower for term in ["fabric", "sda", "sd-access", "virtual network", "site provision"]):
        return "sda"
    elif any(term in query_lower for term in ["device", "inventory", "network device", "switch", "router"]):
        return "devices"
    elif any(term in query_lower for term in ["task", "job", "status", "operation"]):
        return "task"
    
    # Return domain with highest score, default to 'network_inventory' if no clear match
    if domain_scores:
        best_domain = max(domain_scores.items(), key=lambda x: x[1])
        if best_domain[1] > 0:
            return best_domain[0]
    
    return "sda"  # Default fallback


def load_domain_agent(domain_name):
    """Dynamically load and return a domain-specific agent."""
    if domain_name in domain_agents:
        return domain_agents[domain_name]

    try:        # Map abstract domain names to actual agent modules
        domain_mapping = {
            "authentication": "authentication",  # Authentication APIs are in authentication module
            "appliance": "devices",   # Appliance APIs are device-related
            "system": "devices",      # System APIs are in devices
            "connectivity": "sda",    # Connectivity includes SDA
            "ecosystem": "task",      # ITSM integrations are task-related
            "events": "task",         # Event management is task-related
            "network_inventory": "devices",  # Network inventory is devices
            "operational_tasks": "task",     # Operational tasks
            "policy": "sda",          # Policy is SDA-related
            "site_management": "devices",    # Site management is device-related
            "system_settings": "devices",    # System settings are device-related
            "assurance": "devices",          # Assurance is device health
            "sda": "sda",             # Direct SDA mapping
            "devices": "devices",     # Direct devices mapping
            "task": "task"            # Direct task mapping
        }
        
        actual_module = domain_mapping.get(domain_name, domain_name)
        
        # Dynamically import the domain's tools module
        module = importlib.import_module(f"agents.{actual_module}.tools")
        # The module should have a variable named 'agent'
        domain_agent = getattr(module, "agent")
        domain_agents[domain_name] = domain_agent
        return domain_agent
    except (ImportError, AttributeError) as e:
        print(f"Error loading domain agent '{domain_name}': {e}")
        return None


@router_agent.tool()
async def route_authentication_requests(query: str) -> str:
    """
    Use this for requests about authentication, user management, certificates, login, tokens, or credential management.
    
    Examples: "authenticate to system", "manage users", "certificate configuration", "login issues"
    """
    agent = load_domain_agent("authentication")
    if agent and hasattr(agent, 'run_tools'):
        return await agent.run_tools(query)
    return "Error: Could not load the authentication agent."


@router_agent.tool()
async def route_appliance_requests(query: str) -> str:
    """
    Use this for requests about Cisco IMC appliances, hardware management, or server administration.
    
    Examples: "IMC configuration", "appliance status", "hardware health", "server management"
    """
    agent = load_domain_agent("appliance")
    if agent and hasattr(agent, 'run_tools'):
        return await agent.run_tools(query)
    return "Error: Could not load the appliance agent."


@router_agent.tool()
async def route_system_requests(query: str) -> str:
    """
    Use this for requests about system backup, restore, disaster recovery, health monitoring, performance, platform management, licenses, certificates, users, and roles.
    
    Examples: "backup system", "restore configuration", "system health", "license management", "user roles"
    """
    agent = load_domain_agent("system")
    if agent and hasattr(agent, 'run_tools'):
        return await agent.run_tools(query)
    return "Error: Could not load the system agent."


@router_agent.tool()
async def route_connectivity_requests(query: str) -> str:
    """
    Use this for requests about network connectivity including Fabric Wireless, SDA (Software-Defined Access), wired connections, and wireless management.
    
    Examples: "fabric configuration", "SDA setup", "wireless access points", "wired connectivity", "SD-Access policies"
    """
    agent = load_domain_agent("connectivity")
    if agent and hasattr(agent, 'run_tools'):
        return await agent.run_tools(query)
    return "Error: Could not load the connectivity agent."


@router_agent.tool()
async def route_ecosystem_requests(query: str) -> str:
    """
    Use this for requests about ecosystem integrations, particularly ITSM (IT Service Management) integrations and third-party system connections.
    
    Examples: "ITSM integration", "ServiceNow connection", "third-party integrations", "external system APIs"
    """
    agent = load_domain_agent("ecosystem")
    if agent and hasattr(agent, 'run_tools'):
        return await agent.run_tools(query)
    return "Error: Could not load the ecosystem agent."


@router_agent.tool()
async def route_event_requests(query: str) -> str:
    """
    Use this for requests about event management, notifications, alerts, and event processing.
    
    Examples: "event notifications", "alert configuration", "event processing", "notification settings"
    """
    agent = load_domain_agent("events")
    if agent and hasattr(agent, 'run_tools'):
        return await agent.run_tools(query)
    return "Error: Could not load the event management agent."


@router_agent.tool()
async def route_network_inventory_requests(query: str) -> str:
    """
    Use this for requests about network inventory including devices, clients, applications, compliance, devices, EoX information, industrial configuration, issues, security advisories, sensors, sites, topology, and users.
    
    Examples: "device inventory", "client information", "compliance reports", "EoX status", "security advisories", "site topology", "network users"
    """
    agent = load_domain_agent("network_inventory")
    if agent and hasattr(agent, 'run_tools'):
        return await agent.run_tools(query)
    return "Error: Could not load the network inventory agent."


@router_agent.tool()
async def route_operational_tasks_requests(query: str) -> str:
    """
    Use this for requests about operational tasks including command execution, network discovery, file operations, path tracing, reports generation, tagging, and general task management.
    
    Examples: "run command", "discover devices", "generate report", "path trace", "file operations", "task status", "device discovery"
    """
    agent = load_domain_agent("operational_tasks")
    if agent and hasattr(agent, 'run_tools'):
        return await agent.run_tools(query)
    return "Error: Could not load the operational tasks agent."


@router_agent.tool()
async def route_policy_requests(query: str) -> str:
    """
    Use this for requests about AI Endpoint Analytics and Application Policy management.
    
    Examples: "endpoint analytics", "application policies", "AI analytics", "policy configuration", "endpoint behavior"
    """
    agent = load_domain_agent("policy")
    if agent and hasattr(agent, 'run_tools'):
        return await agent.run_tools(query)
    return "Error: Could not load the policy agent."


@router_agent.tool()
async def route_site_management_requests(query: str) -> str:
    """
    Use this for requests about site management including configuration archives, configuration templates, device onboarding (PnP), device replacement, LAN automation, network settings, site design, and software image management (SWIM).
    
    Examples: "configuration template", "device onboarding", "PnP", "LAN automation", "site design", "software image", "SWIM", "device replacement"
    """
    agent = load_domain_agent("site_management")
    if agent and hasattr(agent, 'run_tools'):
        return await agent.run_tools(query)
    return "Error: Could not load the site management agent."


@router_agent.tool()
async def route_system_settings_requests(query: str) -> str:
    """
    Use this for requests about system settings and general system configuration.
    
    Examples: "system settings", "global configuration", "system preferences", "configuration parameters"
    """
    agent = load_domain_agent("system_settings")
    if agent and hasattr(agent, 'run_tools'):
        return await agent.run_tools(query)
    return "Error: Could not load the system settings agent."


@router_agent.tool()
async def route_assurance_requests(query: str) -> str:
    """
    Use this for requests about network assurance, monitoring, analytics, health checking, performance monitoring, and issue resolution.
    
    Examples: "network health", "performance monitoring", "assurance analytics", "network issues", "monitoring dashboards"
    """
    agent = load_domain_agent("assurance")
    if agent and hasattr(agent, 'run_tools'):
        return await agent.run_tools(query)
    return "Error: Could not load the assurance agent."


# Legacy support for existing domain tools (backwards compatibility)
@router_agent.tool()
async def use_device_inventory_tools(query: str) -> str:
    """
    Legacy support: Use this for any request about device inventory, device details, device health, device configuration, or anything else related to network device management.
    """
    return await route_network_inventory_requests(query)


@router_agent.tool()
async def use_sda_tools(query: str) -> str:
    """
    Legacy support: Use this for any request related to Software-Defined Access (SDA), including fabrics, virtual networks, and site provisioning.
    """
    agent = load_domain_agent("sda")
    if agent and hasattr(agent, 'run_tools'):
        return await agent.run_tools(query)
    return "Error: Could not load the sda agent."


@router_agent.tool()
async def use_task_tools(query: str) -> str:
    """
    Legacy support: Use this for any request related to operational tasks, such as checking task status or retrieving task output.
    """
    return await route_operational_tasks_requests(query)


@router_agent.tool()
async def intelligent_route(query: str) -> str:
    """
    Automatically route user queries to the most appropriate domain agent based on intelligent content analysis.
    Use this when you're unsure which specific domain tool to use.
    
    Examples: Any natural language query about Cisco Catalyst Center operations
    """
    domain = classify_query(query)
    
    # Route to appropriate domain
    domain_routing = {
        "authentication": route_authentication_requests,
        "appliance": route_appliance_requests,
        "system": route_system_requests,
        "connectivity": route_connectivity_requests,
        "ecosystem": route_ecosystem_requests,
        "events": route_event_requests,
        "network_inventory": route_network_inventory_requests,
        "operational_tasks": route_operational_tasks_requests,
        "policy": route_policy_requests,
        "site_management": route_site_management_requests,
        "system_settings": route_system_settings_requests,
        "assurance": route_assurance_requests,
        "sda": route_connectivity_requests,  # Direct SDA mapping
        "devices": route_network_inventory_requests,  # Direct devices mapping
        "task": route_operational_tasks_requests  # Direct task mapping
    }
    
    route_function = domain_routing.get(domain, route_network_inventory_requests)
    return await route_function(query)
