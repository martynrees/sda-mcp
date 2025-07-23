import importlib

from mcp_instance import create_mcp_instance

# Create the main router agent
router_agent = create_mcp_instance("RouterAgent")

# In-memory cache for loaded domain agents
domain_agents = {}


def load_domain_agent(domain_name):
    """Dynamically load and return a domain-specific agent."""
    if domain_name in domain_agents:
        return domain_agents[domain_name]

    try:
        # Dynamically import the domain's tools module
        module = importlib.import_module(f"agents.{domain_name}.tools")
        # The module should have a variable named 'agent'
        domain_agent = getattr(module, "agent")
        domain_agents[domain_name] = domain_agent
        return domain_agent
    except (ImportError, AttributeError) as e:
        print(f"Error loading domain agent '{domain_name}': {e}")
        return None


@router_agent.tool()
def use_device_inventory_tools(query: str):
    """
    Use this for any request about device inventory, device details, device health, device configuration,
    or anything else related to network device management.
    """
    agent = load_domain_agent("devices")
    if agent:
        return agent.process_request(query)
    return "Error: Could not load the device inventory agent."


@router_agent.tool()
def use_sda_tools(query: str):
    """
    Use this for any request related to Software-Defined Access (SDA), including fabrics,
    virtual networks, and site provisioning.
    """
    agent = load_domain_agent("sda")
    if agent:
        return agent.process_request(query)
    return "Error: Could not load the SDA agent."


@router_agent.tool()
def use_task_tools(query: str):
    """
    Use this for any request related to operational tasks, such as checking task status or retrieving task output.
    """
    agent = load_domain_agent("task")
    if agent:
        return agent.process_request(query)
    return "Error: Could not load the task agent."
