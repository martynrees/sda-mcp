from typing import Any, Dict, Optional

from client import CatalystCenterClient, client_manager
from mcp_instance import create_mcp_instance
from agents.base_agent import SmartDomainAgent, format_response, extract_parameters_from_query

agent = create_mcp_instance("SDAAgent")

# Create smart domain agent wrapper
sda_tool_keywords = {
    "connect": ["connect", "login", "auth", "authenticate"],
    "get_sites": ["site", "sites", "location", "locations"],
    "get_network_devices": ["device", "devices", "equipment", "network", "switch", "router"],
    "get_edge_device_from_sda_fabric": ["edge", "fabric", "sda"],
    "get_device_info_from_sda_fabric": ["device info", "fabric device", "sda device"],
    "add_site_in_sda_fabric": ["add site", "create site", "provision site"],
    "get_site_from_sda_fabric": ["get site", "site info", "fabric site"],
    "get_vn_from_sda_fabric": ["virtual network", "vn", "layer3", "l3"],
    "add_vn_in_fabric": ["add virtual network", "create vn", "provision vn"],
    "get_fabric_sites": ["fabric sites", "sda sites", "fabric locations"],
    "get_anycast_gateways": ["anycast", "gateway", "gateways"],
    "get_multicast_virtual_networks": ["multicast", "multicast vn", "multicast networks"],
    "get_port_assignments": ["port", "port assignment", "interface assignment"],
    "get_layer2_virtual_networks": ["layer2", "l2", "vlan", "layer 2"],
    "get_layer3_virtual_networks": ["layer3", "l3", "routing", "layer 3"],
    "get_fabric_devices": ["fabric device", "sda device", "fabric equipment"],
    "provision_devices": ["provision", "deploy", "configure device"],
    "get_transit_networks": ["transit", "transit network", "underlay"]
}

smart_agent = SmartDomainAgent("SDA", agent, sda_tool_keywords)


@agent.tool()
async def get_edge_device_from_sda_fabric(deviceManagementIpAddress: str) -> Optional[Dict[str, Any]]:
    """Get edge device from SDA Fabric

    Args:
        deviceManagementIpAddress: deviceManagementIpAddress
    """
    client = client_manager.get_client()
    if not client:
        return {"error": "Not connected. Use connect() first."}

    kwargs = {}
    params = {}
    if deviceManagementIpAddress is not None:
        params["deviceManagementIpAddress"] = deviceManagementIpAddress
    if params:
        kwargs["params"] = params
    return await client.request("GET", f"/dna/intent/api/v1/business/sda/edge-device", **kwargs)


@agent.tool()
async def connect(base_url: str, username: str, password: str) -> str:
    """Connect to Cisco Catalyst Center.

    Args:
        base_url: Base URL of the Catalyst Center (e.g., https://10.10.10.10)
        username: Username for authentication
        password: Password for authentication
    """
    client = CatalystCenterClient(base_url, username, password)
    if await client.authenticate():
        client_manager.set_client(client)
        return "Successfully connected to Cisco Catalyst Center"
    return "Failed to connect to Cisco Catalyst Center"


@agent.tool()
async def get_device_info_from_sda_fabric(deviceManagementIpAddress: str) -> Optional[Dict[str, Any]]:
    """Get device info from SDA Fabric

    Args:
        deviceManagementIpAddress: deviceManagementIpAddress
    """
    client = client_manager.get_client()
    if not client:
        return {"error": "Not connected. Use connect() first."}

    kwargs = {}
    params = {}
    if deviceManagementIpAddress is not None:
        params["deviceManagementIpAddress"] = deviceManagementIpAddress
    if params:
        kwargs["params"] = params
    return await client.request("GET", f"/dna/intent/api/v1/business/sda/device", **kwargs)


@agent.tool()
async def add_ip_pool_in_sda_virtual_network(request_body: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Add IP Pool in SDA Virtual Network

    Args:
        request_body: Request body data
    """
    client = client_manager.get_client()
    if not client:
        return {"error": "Not connected. Use connect() first."}

    kwargs = {}
    kwargs["json"] = request_body
    return await client.request("POST", f"/dna/intent/api/v1/business/sda/virtualnetwork/ippool", **kwargs)


@agent.tool()
async def delete_ip_pool_from_sda_virtual_network(
    siteNameHierarchy: str, virtualNetworkName: str, ipPoolName: str
) -> Optional[Dict[str, Any]]:
    """Delete IP Pool from SDA Virtual Network

    Args:
        siteNameHierarchy: siteNameHierarchy
        virtualNetworkName: virtualNetworkName
        ipPoolName: ipPoolName
    """
    client = client_manager.get_client()
    if not client:
        return {"error": "Not connected. Use connect() first."}

    kwargs = {}
    params = {}
    if siteNameHierarchy is not None:
        params["siteNameHierarchy"] = siteNameHierarchy
    if virtualNetworkName is not None:
        params["virtualNetworkName"] = virtualNetworkName
    if ipPoolName is not None:
        params["ipPoolName"] = ipPoolName
    if params:
        kwargs["params"] = params
    return await client.request("DELETE", f"/dna/intent/api/v1/business/sda/virtualnetwork/ippool", **kwargs)


@agent.tool()
async def get_ip_pool_from_sda_virtual_network(
    siteNameHierarchy: str, virtualNetworkName: str, ipPoolName: str
) -> Optional[Dict[str, Any]]:
    """Get IP Pool from SDA Virtual Network

    Args:
        siteNameHierarchy: siteNameHierarchy
        virtualNetworkName: virtualNetworkName
        ipPoolName: ipPoolName. Note: Use vlanName as a value for this parameter if same ip pool is assigned to multiple virtual networks (e.g.. ipPoolName=vlan1021)
    """
    client = client_manager.get_client()
    if not client:
        return {"error": "Not connected. Use connect() first."}

    kwargs = {}
    params = {}
    if siteNameHierarchy is not None:
        params["siteNameHierarchy"] = siteNameHierarchy
    if virtualNetworkName is not None:
        params["virtualNetworkName"] = virtualNetworkName
    if ipPoolName is not None:
        params["ipPoolName"] = ipPoolName
    if params:
        kwargs["params"] = params
    return await client.request("GET", f"/dna/intent/api/v1/business/sda/virtualnetwork/ippool", **kwargs)


@agent.tool()
async def get_site_from_sda_fabric(siteNameHierarchy: str) -> Optional[Dict[str, Any]]:
    """Get Site from SDA Fabric

    Get Site info from SDA Fabric

    Args:
        siteNameHierarchy: Site Name Hierarchy
    """
    client = client_manager.get_client()
    if not client:
        return {"error": "Not connected. Use connect() first."}

    kwargs = {}
    params = {}
    if siteNameHierarchy is not None:
        params["siteNameHierarchy"] = siteNameHierarchy
    if params:
        kwargs["params"] = params
    return await client.request("GET", f"/dna/intent/api/v1/business/sda/fabric-site", **kwargs)


@agent.tool()
async def add_site_in_sda_fabric(request_body: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Add Site in SDA Fabric

    Args:
        request_body: Request body data
    """
    client = client_manager.get_client()
    if not client:
        return {"error": "Not connected. Use connect() first."}

    kwargs = {}
    kwargs["json"] = request_body
    return await client.request("POST", f"/dna/intent/api/v1/business/sda/fabric-site", **kwargs)


@agent.tool()
async def get_multicast_details_from_sda_fabric(siteNameHierarchy: str) -> Optional[Dict[str, Any]]:
    """Get multicast details from SDA fabric

    Args:
        siteNameHierarchy: fabric site name hierarchy
    """
    client = client_manager.get_client()
    if not client:
        return {"error": "Not connected. Use connect() first."}

    kwargs = {}
    params = {}
    if siteNameHierarchy is not None:
        params["siteNameHierarchy"] = siteNameHierarchy
    if params:
        kwargs["params"] = params
    return await client.request("GET", f"/dna/intent/api/v1/business/sda/multicast", **kwargs)


@agent.tool()
async def add_vn_in_fabric(request_body: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Add VN in fabric

    Add virtual network (VN) in SDA Fabric

    Args:
        request_body: Request body data
    """
    client = client_manager.get_client()
    if not client:
        return {"error": "Not connected. Use connect() first."}

    kwargs = {}
    kwargs["json"] = request_body
    return await client.request("POST", f"/dna/intent/api/v1/business/sda/virtual-network", **kwargs)


@agent.tool()
async def get_vn_from_sda_fabric(virtualNetworkName: str, siteNameHierarchy: str) -> Optional[Dict[str, Any]]:
    """Get VN from SDA Fabric

    Get virtual network (VN) from SDA Fabric

    Args:
        virtualNetworkName: virtualNetworkName
        siteNameHierarchy: siteNameHierarchy
    """
    client = client_manager.get_client()
    if not client:
        return {"error": "Not connected. Use connect() first."}

    kwargs = {}
    params = {}
    if virtualNetworkName is not None:
        params["virtualNetworkName"] = virtualNetworkName
    if siteNameHierarchy is not None:
        params["siteNameHierarchy"] = siteNameHierarchy
    if params:
        kwargs["params"] = params
    return await client.request("GET", f"/dna/intent/api/v1/business/sda/virtual-network", **kwargs)


@agent.tool()
async def delete_vn_from_sda_fabric(virtualNetworkName: str, siteNameHierarchy: str) -> Optional[Dict[str, Any]]:
    """Delete VN from SDA Fabric

    Delete virtual network (VN) from SDA Fabric

    Args:
        virtualNetworkName: virtualNetworkName
        siteNameHierarchy: siteNameHierarchy
    """
    client = client_manager.get_client()
    if not client:
        return {"error": "Not connected. Use connect() first."}

    kwargs = {}
    params = {}
    if virtualNetworkName is not None:
        params["virtualNetworkName"] = virtualNetworkName
    if siteNameHierarchy is not None:
        params["siteNameHierarchy"] = siteNameHierarchy
    if params:
        kwargs["params"] = params
    return await client.request("DELETE", f"/dna/intent/api/v1/business/sda/virtual-network", **kwargs)


@agent.tool()
async def re_provision_wired_device(request_body: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Re-Provision Wired Device

    Args:
        request_body: Request body data
    """
    client = client_manager.get_client()
    if not client:
        return {"error": "Not connected. Use connect() first."}

    kwargs = {}
    kwargs["json"] = request_body
    return await client.request("PUT", f"/dna/intent/api/v1/business/sda/provision-device", **kwargs)


@agent.tool()
async def provision_wired_device(request_body: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Provision Wired Device

    Args:
        request_body: Request body data
    """
    client = client_manager.get_client()
    if not client:
        return {"error": "Not connected. Use connect() first."}

    kwargs = {}
    kwargs["json"] = request_body
    return await client.request("POST", f"/dna/intent/api/v1/business/sda/provision-device", **kwargs)


@agent.tool()
async def get_provisioned_wired_device(deviceManagementIpAddress: str) -> Optional[Dict[str, Any]]:
    """Get Provisioned Wired Device

    Args:
        deviceManagementIpAddress: deviceManagementIpAddress
    """
    client = client_manager.get_client()
    if not client:
        return {"error": "Not connected. Use connect() first."}

    kwargs = {}
    params = {}
    if deviceManagementIpAddress is not None:
        params["deviceManagementIpAddress"] = deviceManagementIpAddress
    if params:
        kwargs["params"] = params
    return await client.request("GET", f"/dna/intent/api/v1/business/sda/provision-device", **kwargs)


@agent.tool()
async def get_virtual_network_summary(siteNameHierarchy: str) -> Optional[Dict[str, Any]]:
    """Get Virtual Network Summary

    Args:
        siteNameHierarchy: Complete fabric siteNameHierarchy Path
    """
    client = client_manager.get_client()
    if not client:
        return {"error": "Not connected. Use connect() first."}

    kwargs = {}
    params = {}
    if siteNameHierarchy is not None:
        params["siteNameHierarchy"] = siteNameHierarchy
    if params:
        kwargs["params"] = params
    return await client.request("GET", f"/dna/intent/api/v1/business/sda/virtual-network/summary", **kwargs)


@agent.tool()
async def add_port_assignment_for_user_device_in_sda_fabric(request_body: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Add Port assignment for user device in SDA Fabric

    Add Port assignment for user device in SDA Fabric.

    Args:
        request_body: Request body data
    """
    client = client_manager.get_client()
    if not client:
        return {"error": "Not connected. Use connect() first."}

    kwargs = {}
    kwargs["json"] = request_body
    return await client.request("POST", f"/dna/intent/api/v1/business/sda/hostonboarding/user-device", **kwargs)


@agent.tool()
async def get_port_assignment_for_user_device_in_sda_fabric(
    deviceManagementIpAddress: str, interfaceName: str
) -> Optional[Dict[str, Any]]:
    """Get Port assignment for user device in SDA Fabric

    Get Port assignment for user device in SDA Fabric.

    Args:
        deviceManagementIpAddress: deviceManagementIpAddress
        interfaceName: interfaceName
    """
    client = client_manager.get_client()
    if not client:
        return {"error": "Not connected. Use connect() first."}

    kwargs = {}
    params = {}
    if deviceManagementIpAddress is not None:
        params["deviceManagementIpAddress"] = deviceManagementIpAddress
    if interfaceName is not None:
        params["interfaceName"] = interfaceName
    if params:
        kwargs["params"] = params
    return await client.request("GET", f"/dna/intent/api/v1/business/sda/hostonboarding/user-device", **kwargs)


@agent.tool()
async def get_control_plane_device_from_sda_fabric(deviceManagementIpAddress: str) -> Optional[Dict[str, Any]]:
    """Get control plane device from SDA Fabric

    Args:
        deviceManagementIpAddress: deviceManagementIpAddress
    """
    client = client_manager.get_client()
    if not client:
        return {"error": "Not connected. Use connect() first."}

    kwargs = {}
    params = {}
    if deviceManagementIpAddress is not None:
        params["deviceManagementIpAddress"] = deviceManagementIpAddress
    if params:
        kwargs["params"] = params
    return await client.request("GET", f"/dna/intent/api/v1/business/sda/control-plane-device", **kwargs)


@agent.tool()  # TODO: move to a more appropriate module
async def get_sites() -> str:
    """Get list of sites in the network."""
    client = client_manager.get_client()
    if not client:
        return "Not connected to Catalyst Center. Use connect() first."

    endpoint = "/dna/intent/api/v1/site"
    data = await client.request("GET", endpoint)

    if not data or "response" not in data:
        return "Unable to fetch sites or no sites found."

    sites = data["response"]
    if not sites:
        return "No sites found."

    formatted_sites = []
    for site in sites:
        formatted = f"""
Site Name: {site.get('name', 'Unknown')}
Site ID: {site.get('id', 'Unknown')}
Type: {site.get('siteType', 'Unknown')}
Parent: {site.get('parentName', 'None')}
"""
        formatted_sites.append(formatted)

    return "\n---\n".join(formatted_sites)


@agent.tool()  # TODO: move to a more appropriate module
async def get_network_devices(limit: int = 10, offset: int = 1) -> str:
    """Get list of network devices.

    Args:
        limit: Maximum number of devices to return (default: 10)
        offset: Pagination offset (default: 1)
    """
    client = client_manager.get_client()
    if not client:
        return "Not connected to Catalyst Center. Use connect() first."

    endpoint = f"/dna/intent/api/v1/network-device?limit={limit}&offset={offset}"
    data = await client.request("GET", endpoint)

    if not data or "response" not in data:
        return "Unable to fetch network devices or no devices found."

    devices = data["response"]
    if not devices:
        return "No network devices found."

    formatted_devices = []
    for device in devices:
        formatted = f"""
                    Device: {device.get('hostname', 'Unknown')}
                    IP: {device.get('managementIpAddress', 'Unknown')}
                    Platform: {device.get('platformId', 'Unknown')}
                    Serial: {device.get('serialNumber', 'Unknown')}
                    Status: {device.get('reachabilityStatus', 'Unknown')}
                    Uptime: {device.get('upTime', 'Unknown')}
                    Software: {device.get('softwareVersion', 'Unknown')}
                    Device ID: {device.get('id', 'N/A')}
                    """
        formatted_devices.append(formatted)

    return "\n---\n".join(formatted_devices)


@agent.tool()
async def add_multicast_virtual_networks(request_body: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """
    Add multicast virtual networks.

    Args:
        request_body: The request body containing multicast configurations for virtual networks.
    """
    client = client_manager.get_client()
    if not client:
        return {"error": "Not connected. Use connect() first."}

    kwargs = {"json": request_body}
    return await client.request("POST", "/dna/intent/api/v1/sda/multicast/virtualNetworks", **kwargs)


@agent.tool()
async def get_multicast_virtual_networks(
    fabricId: Optional[str] = None,
    virtualNetworkName: Optional[str] = None,
    offset: Optional[float] = None,
    limit: Optional[float] = None,
) -> Optional[Dict[str, Any]]:
    """
    Get multicast virtual networks.

    Args:
        fabricId: ID of the fabric site where multicast is configured.
        virtualNetworkName: Name of the virtual network associated to the multicast configuration.
        offset: Starting record for pagination.
        limit: Maximum number of records to return (max 500).
    """
    client = client_manager.get_client()
    if not client:
        return {"error": "Not connected. Use connect() first."}

    kwargs = {}
    params = {}
    if fabricId is not None:
        params["fabricId"] = fabricId
    if virtualNetworkName is not None:
        params["virtualNetworkName"] = virtualNetworkName
    if offset is not None:
        params["offset"] = offset
    if limit is not None:
        params["limit"] = limit
    if params:
        kwargs["params"] = params

    return await client.request("GET", "/dna/intent/api/v1/sda/multicast/virtualNetworks", **kwargs)


@agent.tool()
async def update_multicast_virtual_networks(request_body: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """
    Update multicast virtual networks.

    Args:
        request_body: The request body containing updated multicast configurations for virtual networks.
    """
    client = client_manager.get_client()
    if not client:
        return {"error": "Not connected. Use connect() first."}

    kwargs = {"json": request_body}
    return await client.request("PUT", "/dna/intent/api/v1/sda/multicast/virtualNetworks", **kwargs)


@agent.tool()
async def delete_multicast_virtual_network_by_id(
    id: str,
) -> Optional[Dict[str, Any]]:
    """
    Delete multicast virtual network by id.

    Args:
        id: ID of the multicast configuration to delete.
    """
    client = client_manager.get_client()
    if not client:
        return {"error": "Not connected. Use connect() first."}

    return await client.request("DELETE", f"/dna/intent/api/v1/sda/multicast/virtualNetworks/{id}")


@agent.tool()
async def read_transit_network_with_its_health_summary_from_id(
    id: str,
    x_caller_id: Optional[str] = None,
    endTime: Optional[float] = None,
    startTime: Optional[float] = None,
    attribute: Optional[str] = None,
    view: Optional[str] = None,
) -> Optional[Dict[str, Any]]:
    """
    Read transit network with its health summary from id.

    Args:
        id: The unique transit network id.
        x_caller_id: Optional caller ID to trace API calls.
        endTime: End time for the data query in UNIX epoch milliseconds.
        startTime: Start time for the data query in UNIX epoch milliseconds.
        attribute: The interested fields in the request.
        view: The specific summary view being requested.
    """
    client = client_manager.get_client()
    if not client:
        return {"error": "Not connected. Use connect() first."}

    kwargs = {}
    headers = {}
    if x_caller_id is not None:
        headers["X-CALLER-ID"] = x_caller_id
    if headers:
        kwargs["headers"] = headers

    params = {}
    if endTime is not None:
        params["endTime"] = endTime
    if startTime is not None:
        params["startTime"] = startTime
    if attribute is not None:
        params["attribute"] = attribute
    if view is not None:
        params["view"] = view
    if params:
        kwargs["params"] = params

    return await client.request("GET", f"/dna/data/api/v1/transitNetworkHealthSummaries/{id}", **kwargs)


@agent.tool()
async def update_layer3_virtual_networks(request_body: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """
    Update layer 3 virtual networks.

    Args:
        request_body: The request body containing the layer 3 virtual network updates.
    """
    client = client_manager.get_client()
    if not client:
        return {"error": "Not connected. Use connect() first."}

    kwargs = {"json": request_body}
    return await client.request("PUT", "/dna/intent/api/v1/sda/layer3VirtualNetworks", **kwargs)


@agent.tool()
async def add_port_channels(request_body: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """
    Add port channels.

    Args:
        request_body: The request body containing the port channel configurations to add.
    """
    client = client_manager.get_client()
    if not client:
        return {"error": "Not connected. Use connect() first."}

    kwargs = {"json": request_body}
    return await client.request("POST", "/dna/intent/api/v1/sda/portChannels", **kwargs)


@agent.tool()
async def update_port_channels(request_body: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """
    Update port channels.

    Args:
        request_body: The request body containing the port channel configurations to update.
    """
    client = client_manager.get_client()
    if not client:
        return {"error": "Not connected. Use connect() first."}

    kwargs = {"json": request_body}
    return await client.request("PUT", "/dna/intent/api/v1/sda/portChannels", **kwargs)


@agent.tool()
async def delete_port_channels(
    fabricId: str,
    networkDeviceId: Optional[str] = None,
    portChannelName: Optional[str] = None,
    portChannelIds: Optional[str] = None,
    connectedDeviceType: Optional[str] = None,
) -> Optional[Dict[str, Any]]:
    """
    Delete port channels.

    Args:
        fabricId: ID of the fabric the device is assigned to.
        networkDeviceId: ID of the network device.
        portChannelName: Name of the port channel.
        portChannelIds: Comma-separated IDs of the port channels to be selectively deleted.
        connectedDeviceType: Connected device type of the port channel (TRUNK or EXTENDED_NODE).
    """
    client = client_manager.get_client()
    if not client:
        return {"error": "Not connected. Use connect() first."}

    kwargs = {}
    params = {"fabricId": fabricId}
    if networkDeviceId is not None:
        params["networkDeviceId"] = networkDeviceId
    if portChannelName is not None:
        params["portChannelName"] = portChannelName
    if portChannelIds is not None:
        params["portChannelIds"] = portChannelIds
    if connectedDeviceType is not None:
        params["connectedDeviceType"] = connectedDeviceType
    if params:
        kwargs["params"] = params

    return await client.request("DELETE", "/dna/intent/api/v1/sda/portChannels", **kwargs)


@agent.tool()
async def get_port_channels(
    fabricId: Optional[str] = None,
    networkDeviceId: Optional[str] = None,
    portChannelName: Optional[str] = None,
    connectedDeviceType: Optional[str] = None,
    nativeVlanId: Optional[float] = None,
    offset: Optional[float] = None,
    limit: Optional[float] = None,
) -> Optional[Dict[str, Any]]:
    """
    Get port channels.

    Args:
        fabricId: ID of the fabric the device is assigned to.
        networkDeviceId: ID of the network device.
        portChannelName: Name of the port channel.
        connectedDeviceType: Connected device type of the port channel (TRUNK or EXTENDED_NODE).
        nativeVlanId: Native VLAN of the port channel (for TRUNK type).
        offset: Starting record for pagination.
        limit: Maximum number of records to return (max 500).
    """
    client = client_manager.get_client()
    if not client:
        return {"error": "Not connected. Use connect() first."}

    kwargs = {}
    params = {}
    if fabricId is not None:
        params["fabricId"] = fabricId
    if networkDeviceId is not None:
        params["networkDeviceId"] = networkDeviceId
    if portChannelName is not None:
        params["portChannelName"] = portChannelName
    if connectedDeviceType is not None:
        params["connectedDeviceType"] = connectedDeviceType
    if nativeVlanId is not None:
        params["nativeVlanId"] = nativeVlanId
    if offset is not None:
        params["offset"] = offset
    if limit is not None:
        params["limit"] = limit
    if params:
        kwargs["params"] = params

    return await client.request("GET", "/dna/intent/api/v1/sda/portChannels", **kwargs)


@agent.tool()
async def delete_fabric_device_layer3_handoffs_with_sda_transit(
    fabricId: str, networkDeviceId: str
) -> Optional[Dict[str, Any]]:
    """
    Delete fabric device layer 3 handoffs with sda transit.

    Args:
        fabricId: ID of the fabric this device belongs to.
        networkDeviceId: Network device ID of the fabric device.
    """
    client = client_manager.get_client()
    if not client:
        return {"error": "Not connected. Use connect() first."}

    kwargs = {}
    params = {"fabricId": fabricId, "networkDeviceId": networkDeviceId}
    if params:
        kwargs["params"] = params

    return await client.request(
        "DELETE",
        "/dna/intent/api/v1/sda/fabricDevices/layer3Handoffs/sdaTransits",
        **kwargs,
    )


@agent.tool()
async def add_fabric_devices_layer3_handoffs_with_sda_transit(request_body: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """
    Add fabric devices layer 3 handoffs with sda transit.

    Args:
        request_body: The request body containing the layer 3 handoff configurations.
    """
    client = client_manager.get_client()
    if not client:
        return {"error": "Not connected. Use connect() first."}

    kwargs = {"json": request_body}
    return await client.request(
        "POST",
        "/dna/intent/api/v1/sda/fabricDevices/layer3Handoffs/sdaTransits",
        **kwargs,
    )


@agent.tool()
async def update_fabric_devices_layer3_handoffs_with_sda_transit(
    request_body: Dict[str, Any],
) -> Optional[Dict[str, Any]]:
    """
    Update fabric devices layer 3 handoffs with sda transit.

    Args:
        request_body: The request body containing the updated layer 3 handoff configurations.
    """
    client = client_manager.get_client()
    if not client:
        return {"error": "Not connected. Use connect() first."}

    kwargs = {"json": request_body}
    return await client.request(
        "PUT",
        "/dna/intent/api/v1/sda/fabricDevices/layer3Handoffs/sdaTransits",
        **kwargs,
    )


@agent.tool()
async def the_trend_analytics_data_for_a_transit_network_in_the_specified_time_range(
    id: str,
    trendInterval: str,
    x_caller_id: Optional[str] = None,
    startTime: Optional[float] = None,
    endTime: Optional[float] = None,
    limit: Optional[float] = None,
    offset: Optional[float] = None,
    order: Optional[str] = None,
    attribute: Optional[str] = None,
) -> Optional[Dict[str, Any]]:
    """
    Get the Trend analytics data for a transit network in the specified time range.

    Args:
        id: The unique transit network id.
        trendInterval: The time window to aggregate the metrics (e.g., '5 minutes', '1 hour').
        x_caller_id: Optional caller ID to trace API calls.
        startTime: Start time for the data query in UNIX epoch milliseconds.
        endTime: End time for the data query in UNIX epoch milliseconds.
        limit: Maximum number of records to return.
        offset: Starting point for pagination (1-based).
        order: The sort order of the field (ascending or descending).
        attribute: The interested fields in the request.
    """
    client = client_manager.get_client()
    if not client:
        return {"error": "Not connected. Use connect() first."}

    kwargs = {}
    headers = {}
    if x_caller_id is not None:
        headers["X-CALLER-ID"] = x_caller_id
    if headers:
        kwargs["headers"] = headers

    params = {"trendInterval": trendInterval}
    if startTime is not None:
        params["startTime"] = startTime
    if endTime is not None:
        params["endTime"] = endTime
    if limit is not None:
        params["limit"] = limit
    if offset is not None:
        params["offset"] = offset
    if order is not None:
        params["order"] = order
    if attribute is not None:
        params["attribute"] = attribute
    if params:
        kwargs["params"] = params

    return await client.request(
        "GET",
        f"/dna/data/api/v1/transitNetworkHealthSummaries/{id}/trendAnalytics",
        **kwargs,
    )


@agent.tool()
async def add_fabric_devices_layer3_handoffs_with_ip_transit(request_body: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """
    Add fabric devices layer 3 handoffs with ip transit.

    Args:
        request_body: The request body containing the IP transit layer 3 handoff configurations.
    """
    client = client_manager.get_client()
    if not client:
        return {"error": "Not connected. Use connect() first."}

    kwargs = {"json": request_body}
    return await client.request(
        "POST",
        "/dna/intent/api/v1/sda/fabricDevices/layer3Handoffs/ipTransits",
        **kwargs,
    )


@agent.tool()
async def update_fabric_devices_layer3_handoffs_with_ip_transit(
    request_body: Dict[str, Any],
) -> Optional[Dict[str, Any]]:
    """
    Update fabric devices layer 3 handoffs with ip transit.

    Args:
        request_body: The request body containing the updated IP transit layer 3 handoff configurations.
    """
    client = client_manager.get_client()
    if not client:
        return {"error": "Not connected. Use connect() first."}

    kwargs = {"json": request_body}
    return await client.request(
        "PUT",
        "/dna/intent/api/v1/sda/fabricDevices/layer3Handoffs/ipTransits",
        **kwargs,
    )


@agent.tool()
async def delete_fabric_device_layer3_handoffs_with_ip_transit(
    fabricId: str, networkDeviceId: str
) -> Optional[Dict[str, Any]]:
    """
    Delete fabric device layer 3 handoffs with ip transit.

    Args:
        fabricId: ID of the fabric this device belongs to.
        networkDeviceId: Network device ID of the fabric device.
    """
    client = client_manager.get_client()
    if not client:
        return {"error": "Not connected. Use connect() first."}

    kwargs = {}
    params = {"fabricId": fabricId, "networkDeviceId": networkDeviceId}
    if params:
        kwargs["params"] = params

    return await client.request(
        "DELETE",
        "/dna/intent/api/v1/sda/fabricDevices/layer3Handoffs/ipTransits",
        **kwargs,
    )


@agent.tool()
async def get_fabric_devices_layer3_handoffs_with_ip_transit(
    fabricId: str,
    networkDeviceId: Optional[str] = None,
    offset: Optional[float] = None,
    limit: Optional[float] = None,
) -> Optional[Dict[str, Any]]:
    """
    Get fabric devices layer 3 handoffs with ip transit.

    Args:
        fabricId: ID of the fabric this device belongs to.
        networkDeviceId: Network device ID of the fabric device.
        offset: Starting record for pagination.
        limit: Maximum number of records to return (max 500).
    """
    client = client_manager.get_client()
    if not client:
        return {"error": "Not connected. Use connect() first."}

    kwargs = {}
    params = {"fabricId": fabricId}
    if networkDeviceId is not None:
        params["networkDeviceId"] = networkDeviceId
    if offset is not None:
        params["offset"] = offset
    if limit is not None:
        params["limit"] = limit
    if params:
        kwargs["params"] = params

    return await client.request(
        "GET",
        "/dna/intent/api/v1/sda/fabricDevices/layer3Handoffs/ipTransits",
        **kwargs,
    )


@agent.tool()
async def get_extranet_policy_count() -> Optional[Dict[str, Any]]:
    """
    Get extranet policy count.
    """
    client = client_manager.get_client()
    if not client:
        return {"error": "Not connected. Use connect() first."}

    return await client.request("GET", "/dna/intent/api/v1/sda/extranetPolicies/count")


@agent.tool()
async def delete_port_channel_by_id(id: str) -> Optional[Dict[str, Any]]:
    """
    Delete port channel by id.

    Args:
        id: ID of the port channel to delete.
    """
    client = client_manager.get_client()
    if not client:
        return {"error": "Not connected. Use connect() first."}

    return await client.request("DELETE", f"/dna/intent/api/v1/sda/portChannels/{id}")


@agent.tool()
async def get_fabric_devices_layer2_handoffs_count(
    fabricId: str, networkDeviceId: Optional[str] = None
) -> Optional[Dict[str, Any]]:
    """Get fabric devices layer 2 handoffs count

    Returns the count of layer 2 handoffs of fabric devices that match the provided query parameters.

    Args:
        fabricId: ID of the fabric this device belongs to.
        networkDeviceId: Network device ID of the fabric device.
    """
    client = client_manager.get_client()
    if not client:
        return {"error": "Not connected. Use connect() first."}

    kwargs = {}
    params = {"fabricId": fabricId}
    if networkDeviceId is not None:
        params["networkDeviceId"] = networkDeviceId
    kwargs["params"] = params
    return await client.request("GET", "/dna/intent/api/v1/sda/fabricDevices/layer2Handoffs/count", **kwargs)


@agent.tool()
async def get_fabric_site_count() -> Optional[Dict[str, Any]]:
    """Get fabric site count

    Returns the count of fabric sites that match the provided query parameters.
    """
    client = client_manager.get_client()
    if not client:
        return {"error": "Not connected. Use connect() first."}

    return await client.request("GET", "/dna/intent/api/v1/sda/fabricSites/count")


@agent.tool()
async def get_anycast_gateways(
    id: Optional[str] = None,
    fabricId: Optional[str] = None,
    virtualNetworkName: Optional[str] = None,
    ipPoolName: Optional[str] = None,
    vlanName: Optional[str] = None,
    vlanId: Optional[int] = None,
    offset: Optional[int] = None,
    limit: Optional[int] = None,
) -> Optional[Dict[str, Any]]:
    """Get anycast gateways

    Returns a list of anycast gateways that match the provided query parameters.

    Args:
        id: ID of the anycast gateway.
        fabricId: ID of the fabric the anycast gateway is assigned to.
        virtualNetworkName: Name of the virtual network associated with the anycast gateways.
        ipPoolName: Name of the IP pool associated with the anycast gateways.
        vlanName: VLAN name of the anycast gateways.
        vlanId: VLAN ID of the anycast gateways.
        offset: Starting record for pagination.
        limit: Maximum number of records to return (max 500).
    """
    client = client_manager.get_client()
    if not client:
        return {"error": "Not connected. Use connect() first."}

    kwargs = {}
    params = {}
    if id is not None:
        params["id"] = id
    if fabricId is not None:
        params["fabricId"] = fabricId
    if virtualNetworkName is not None:
        params["virtualNetworkName"] = virtualNetworkName
    if ipPoolName is not None:
        params["ipPoolName"] = ipPoolName
    if vlanName is not None:
        params["vlanName"] = vlanName
    if vlanId is not None:
        params["vlanId"] = vlanId
    if offset is not None:
        params["offset"] = offset
    if limit is not None:
        params["limit"] = limit
    if params:
        kwargs["params"] = params
    return await client.request("GET", "/dna/intent/api/v1/sda/anycastGateways", **kwargs)


@agent.tool()
async def add_anycast_gateways(request_body: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Add anycast gateways

    Adds anycast gateways based on user input.

    Args:
        request_body: The request body containing anycast gateway configurations.
    """
    client = client_manager.get_client()
    if not client:
        return {"error": "Not connected. Use connect() first."}

    kwargs = {"json": request_body}
    return await client.request("POST", "/dna/intent/api/v1/sda/anycastGateways", **kwargs)


@agent.tool()
async def get_fabric_zone_count() -> Optional[Dict[str, Any]]:
    """Get fabric zone count

    Returns the count of fabric zones that match the provided query parameters.
    """
    client = client_manager.get_client()
    if not client:
        return {"error": "Not connected. Use connect() first."}

    return await client.request("GET", "/dna/intent/api/v1/sda/fabricZones/count")


@agent.tool()
async def update_layer2_virtual_networks(request_body: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Update layer 2 virtual networks

    Updates layer 2 virtual networks based on user input.

    Args:
        request_body: The request body containing layer 2 virtual network updates.
    """
    client = client_manager.get_client()
    if not client:
        return {"error": "Not connected. Use connect() first."}

    kwargs = {"json": request_body}
    return await client.request("PUT", "/dna/intent/api/v1/sda/layer2VirtualNetworks", **kwargs)


@agent.tool()
async def get_layer2_virtual_networks(
    id: Optional[str] = None,
    fabricId: Optional[str] = None,
    vlanName: Optional[str] = None,
    vlanId: Optional[int] = None,
    trafficType: Optional[str] = None,
    associatedLayer3VirtualNetworkName: Optional[str] = None,
    offset: Optional[int] = None,
    limit: Optional[int] = None,
) -> Optional[Dict[str, Any]]:
    """Get layer 2 virtual networks

    Returns a list of layer 2 virtual networks that match the provided query parameters.

    Args:
        id: ID of the layer 2 virtual network.
        fabricId: ID of the fabric the layer 2 virtual network is assigned to.
        vlanName: The vlan name of the layer 2 virtual network.
        vlanId: The vlan ID of the layer 2 virtual network.
        trafficType: The traffic type of the layer 2 virtual network.
        associatedLayer3VirtualNetworkName: Name of the associated layer 3 virtual network.
        offset: Starting record for pagination.
        limit: Maximum number of records to return (max 500).
    """
    client = client_manager.get_client()
    if not client:
        return {"error": "Not connected. Use connect() first."}

    kwargs = {}
    params = {}
    if id is not None:
        params["id"] = id
    if fabricId is not None:
        params["fabricId"] = fabricId
    if vlanName is not None:
        params["vlanName"] = vlanName
    if vlanId is not None:
        params["vlanId"] = vlanId
    if trafficType is not None:
        params["trafficType"] = trafficType
    if associatedLayer3VirtualNetworkName is not None:
        params["associatedLayer3VirtualNetworkName"] = associatedLayer3VirtualNetworkName
    if offset is not None:
        params["offset"] = offset
    if limit is not None:
        params["limit"] = limit
    if params:
        kwargs["params"] = params
    return await client.request("GET", "/dna/intent/api/v1/sda/layer2VirtualNetworks", **kwargs)


@agent.tool()
async def delete_layer2_virtual_networks(
    fabricId: str,
    vlanName: Optional[str] = None,
    vlanId: Optional[int] = None,
    trafficType: Optional[str] = None,
    associatedLayer3VirtualNetworkName: Optional[str] = None,
) -> Optional[Dict[str, Any]]:
    """Delete layer 2 virtual networks

    Deletes layer 2 virtual networks based on user input.

    Args:
        fabricId: ID of the fabric the layer 2 virtual network is assigned to.
        vlanName: The vlan name of the layer 2 virtual network.
        vlanId: The vlan ID of the layer 2 virtual network.
        trafficType: The traffic type of the layer 2 virtual network.
        associatedLayer3VirtualNetworkName: Name of the associated layer 3 virtual network.
    """
    client = client_manager.get_client()
    if not client:
        return {"error": "Not connected. Use connect() first."}

    kwargs = {}
    params = {"fabricId": fabricId}
    if vlanName is not None:
        params["vlanName"] = vlanName
    if vlanId is not None:
        params["vlanId"] = vlanId
    if trafficType is not None:
        params["trafficType"] = trafficType
    if associatedLayer3VirtualNetworkName is not None:
        params["associatedLayer3VirtualNetworkName"] = associatedLayer3VirtualNetworkName
    kwargs["params"] = params
    return await client.request("DELETE", "/dna/intent/api/v1/sda/layer2VirtualNetworks", **kwargs)


@agent.tool()
async def add_layer2_virtual_networks(request_body: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Add layer 2 virtual networks

    Adds layer 2 virtual networks based on user input.

    Args:
        request_body: The request body containing layer 2 virtual network configurations.
    """
    client = client_manager.get_client()
    if not client:
        return {"error": "Not connected. Use connect() first."}

    kwargs = {"json": request_body}
    return await client.request("POST", "/dna/intent/api/v1/sda/layer2VirtualNetworks", **kwargs)


@agent.tool()
async def get_fabric_devices_layer3_handoffs_with_sda_transit(
    fabricId: str,
    networkDeviceId: Optional[str] = None,
    offset: Optional[int] = None,
    limit: Optional[int] = None,
) -> Optional[Dict[str, Any]]:
    """Get fabric devices layer 3 handoffs with sda transit

    Returns a list of layer 3 handoffs with sda transit of fabric devices that match the provided query parameters.

    Args:
        fabricId: ID of the fabric this device belongs to.
        networkDeviceId: Network device ID of the fabric device.
        offset: Starting record for pagination.
        limit: Maximum number of records to return (max 500).
    """
    client = client_manager.get_client()
    if not client:
        return {"error": "Not connected. Use connect() first."}

    kwargs = {}
    params = {"fabricId": fabricId}
    if networkDeviceId is not None:
        params["networkDeviceId"] = networkDeviceId
    if offset is not None:
        params["offset"] = offset
    if limit is not None:
        params["limit"] = limit
    kwargs["params"] = params
    return await client.request("GET", "/dna/intent/api/v1/sda/fabricDevices/layer3Handoffs/sdaTransits", **kwargs)


@agent.tool()
async def read_list_of_fabric_sites_with_their_health_summary(
    x_caller_id: Optional[str] = None,
    startTime: Optional[float] = None,
    endTime: Optional[float] = None,
    limit: Optional[float] = None,
    offset: Optional[float] = None,
    sortBy: Optional[str] = None,
    order: Optional[str] = None,
    id: Optional[str] = None,
    attribute: Optional[str] = None,
    view: Optional[str] = None,
    siteHierarchy: Optional[str] = None,
    siteHierarchyId: Optional[str] = None,
) -> Optional[Dict[str, Any]]:
    """Read list of Fabric Sites with their health summary

    Get a paginated list of Fabric sites Networks with health summary.

    Args:
        x_caller_id: Optional caller ID to trace API calls.
        startTime: Start time for the data query in UNIX epoch milliseconds.
        endTime: End time for the data query in UNIX epoch milliseconds.
        limit: Maximum number of records to return.
        offset: Starting point for pagination (1-based).
        sortBy: A field within the response to sort by.
        order: The sort order of the field (ascending or descending).
        id: Comma-separated list of entity UUIDs to filter by.
        attribute: List of FabricSite health attributes to include.
        view: The specific summary view being requested.
        siteHierarchy: Full site hierarchy path to filter by.
        siteHierarchyId: Full site hierarchy UUID path to filter by.
    """
    client = client_manager.get_client()
    if not client:
        return {"error": "Not connected. Use connect() first."}

    kwargs = {}
    headers = {}
    if x_caller_id is not None:
        headers["X-CALLER-ID"] = x_caller_id
    if headers:
        kwargs["headers"] = headers

    params = {}
    if startTime is not None:
        params["startTime"] = startTime
    if endTime is not None:
        params["endTime"] = endTime
    if limit is not None:
        params["limit"] = limit
    if offset is not None:
        params["offset"] = offset
    if sortBy is not None:
        params["sortBy"] = sortBy
    if order is not None:
        params["order"] = order
    if id is not None:
        params["id"] = id
    if attribute is not None:
        params["attribute"] = attribute
    if view is not None:
        params["view"] = view
    if siteHierarchy is not None:
        params["siteHierarchy"] = siteHierarchy
    if siteHierarchyId is not None:
        params["siteHierarchyId"] = siteHierarchyId
    if params:
        kwargs["params"] = params
    return await client.request("GET", "/dna/data/api/v1/fabricSiteHealthSummaries", **kwargs)


@agent.tool()
async def get_layer3_virtual_networks(
    virtualNetworkName: Optional[str] = None,
    fabricId: Optional[str] = None,
    anchoredSiteId: Optional[str] = None,
    offset: Optional[int] = None,
    limit: Optional[int] = None,
) -> Optional[Dict[str, Any]]:
    """Get layer 3 virtual networks

    Returns a list of layer 3 virtual networks that match the provided query parameters.

    Args:
        virtualNetworkName: Name of the layer 3 virtual network.
        fabricId: ID of the fabric the layer 3 virtual network is assigned to.
        anchoredSiteId: Fabric ID of the fabric site the layer 3 virtual network is anchored at.
        offset: Starting record for pagination.
        limit: Maximum number of records to return (max 500).
    """
    client = client_manager.get_client()
    if not client:
        return {"error": "Not connected. Use connect() first."}

    kwargs = {}
    params = {}
    if virtualNetworkName is not None:
        params["virtualNetworkName"] = virtualNetworkName
    if fabricId is not None:
        params["fabricId"] = fabricId
    if anchoredSiteId is not None:
        params["anchoredSiteId"] = anchoredSiteId
    if offset is not None:
        params["offset"] = offset
    if limit is not None:
        params["limit"] = limit
    if params:
        kwargs["params"] = params
    return await client.request("GET", "/dna/intent/api/v1/sda/layer3VirtualNetworks", **kwargs)


@agent.tool()
async def delete_layer3_virtual_networks(virtualNetworkName: Optional[str] = None) -> Optional[Dict[str, Any]]:
    """Delete layer 3 virtual networks

    Deletes layer 3 virtual networks based on user input.

    Args:
        virtualNetworkName: Name of the layer 3 virtual network.
    """
    client = client_manager.get_client()
    if not client:
        return {"error": "Not connected. Use connect() first."}

    kwargs = {}
    params = {}
    if virtualNetworkName is not None:
        params["virtualNetworkName"] = virtualNetworkName
    if params:
        kwargs["params"] = params
    return await client.request("DELETE", "/dna/intent/api/v1/sda/layer3VirtualNetworks", **kwargs)


@agent.tool()
async def add_layer3_virtual_networks(request_body: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Add layer 3 virtual networks

    Adds layer 3 virtual networks based on user input.

    Args:
        request_body: The request body containing layer 3 virtual network configurations.
    """
    client = client_manager.get_client()
    if not client:
        return {"error": "Not connected. Use connect() first."}

    kwargs = {"json": request_body}
    return await client.request("POST", "/dna/intent/api/v1/sda/layer3VirtualNetworks", **kwargs)


@agent.tool()
async def read_virtual_network_with_its_health_summary_from_id(
    id: str,
    x_caller_id: Optional[str] = None,
    endTime: Optional[float] = None,
    startTime: Optional[float] = None,
    attribute: Optional[str] = None,
    view: Optional[str] = None,
) -> Optional[Dict[str, Any]]:
    """Read virtual network with its health summary from id

    Get health summary for a specific Virtual Network by providing its unique ID.

    Args:
        id: Unique virtual network ID.
        x_caller_id: Optional caller ID to trace API calls.
        endTime: End time for the data query in UNIX epoch milliseconds.
        startTime: Start time for the data query in UNIX epoch milliseconds.
        attribute: The interested fields in the request.
        view: The specific summary view being requested.
    """
    client = client_manager.get_client()
    if not client:
        return {"error": "Not connected. Use connect() first."}

    kwargs = {}
    headers = {}
    if x_caller_id is not None:
        headers["X-CALLER-ID"] = x_caller_id
    if headers:
        kwargs["headers"] = headers

    params = {}
    if endTime is not None:
        params["endTime"] = endTime
    if startTime is not None:
        params["startTime"] = startTime
    if attribute is not None:
        params["attribute"] = attribute
    if view is not None:
        params["view"] = view
    if params:
        kwargs["params"] = params
    return await client.request("GET", f"/dna/data/api/v1/virtualNetworkHealthSummaries/{id}", **kwargs)


@agent.tool()
async def get_port_assignment_count(
    fabricId: Optional[str] = None,
    networkDeviceId: Optional[str] = None,
    interfaceName: Optional[str] = None,
    dataVlanName: Optional[str] = None,
    voiceVlanName: Optional[str] = None,
) -> Optional[Dict[str, Any]]:
    """Get port assignment count

    Returns the count of port assignments that match the provided query parameters.

    Args:
        fabricId: ID of the fabric the device is assigned to.
        networkDeviceId: Network device ID of the port assignment.
        interfaceName: Interface name of the port assignment.
        dataVlanName: Data VLAN name of the port assignment.
        voiceVlanName: Voice VLAN name of the port assignment.
    """
    client = client_manager.get_client()
    if not client:
        return {"error": "Not connected. Use connect() first."}

    kwargs = {}
    params = {}
    if fabricId is not None:
        params["fabricId"] = fabricId
    if networkDeviceId is not None:
        params["networkDeviceId"] = networkDeviceId
    if interfaceName is not None:
        params["interfaceName"] = interfaceName
    if dataVlanName is not None:
        params["dataVlanName"] = dataVlanName
    if voiceVlanName is not None:
        params["voiceVlanName"] = voiceVlanName
    if params:
        kwargs["params"] = params
    return await client.request("GET", "/dna/intent/api/v1/sda/portAssignments/count", **kwargs)


@agent.tool()
async def get_pending_fabric_events(
    fabricId: Optional[str] = None,
    offset: Optional[int] = None,
    limit: Optional[int] = None,
) -> Optional[Dict[str, Any]]:
    """Get pending fabric events

    Returns a list of pending fabric events that match the provided query parameters.

    Args:
        fabricId: ID of the fabric.
        offset: Starting record for pagination.
        limit: Maximum number of records to return (max 500).
    """
    client = client_manager.get_client()
    if not client:
        return {"error": "Not connected. Use connect() first."}

    kwargs = {}
    params = {}
    if fabricId is not None:
        params["fabricId"] = fabricId
    if offset is not None:
        params["offset"] = offset
    if limit is not None:
        params["limit"] = limit
    if params:
        kwargs["params"] = params
    return await client.request("GET", "/dna/intent/api/v1/sda/pendingFabricEvents", **kwargs)


@agent.tool()
async def reprovision_devices(request_body: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Re-provision devices

    Re-provisions network devices to the site based on the user input.

    Args:
        request_body: The request body containing device re-provisioning information.
    """
    client = client_manager.get_client()
    if not client:
        return {"error": "Not connected. Use connect() first."}

    kwargs = {"json": request_body}
    return await client.request("PUT", "/dna/intent/api/v1/sda/provisionDevices", **kwargs)


@agent.tool()
async def provision_devices(request_body: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Provision devices

    Provisions network devices to respective Sites based on user input.

    Args:
        request_body: The request body containing device provisioning information.
    """
    client = client_manager.get_client()
    if not client:
        return {"error": "Not connected. Use connect() first."}

    kwargs = {"json": request_body}
    return await client.request("POST", "/dna/intent/api/v1/sda/provisionDevices", **kwargs)


@agent.tool()
async def get_provisioned_devices(
    id: Optional[str] = None,
    networkDeviceId: Optional[str] = None,
    siteId: Optional[str] = None,
    offset: Optional[int] = None,
    limit: Optional[int] = None,
) -> Optional[Dict[str, Any]]:
    """Get provisioned devices

    Returns the list of provisioned devices based on query parameters.

    Args:
        id: ID of the provisioned device.
        networkDeviceId: ID of the network device.
        siteId: ID of the site hierarchy.
        offset: Starting record for pagination.
        limit: Maximum number of devices to return (max 500).
    """
    client = client_manager.get_client()
    if not client:
        return {"error": "Not connected. Use connect() first."}

    kwargs = {}
    params = {}
    if id is not None:
        params["id"] = id
    if networkDeviceId is not None:
        params["networkDeviceId"] = networkDeviceId
    if siteId is not None:
        params["siteId"] = siteId
    if offset is not None:
        params["offset"] = offset
    if limit is not None:
        params["limit"] = limit
    if params:
        kwargs["params"] = params
    return await client.request("GET", "/dna/intent/api/v1/sda/provisionDevices", **kwargs)


@agent.tool()
async def get_layer2_virtual_network_count(
    fabricId: Optional[str] = None,
    vlanName: Optional[str] = None,
    vlanId: Optional[int] = None,
    trafficType: Optional[str] = None,
    associatedLayer3VirtualNetworkName: Optional[str] = None,
) -> Optional[Dict[str, Any]]:
    """Get layer 2 virtual network count

    Returns the count of layer 2 virtual networks that match the provided query parameters.

    Args:
        fabricId: ID of the fabric the layer 2 virtual network is assigned to.
        vlanName: The vlan name of the layer 2 virtual network.
        vlanId: The vlan ID of the layer 2 virtual network.
        trafficType: The traffic type of the layer 2 virtual network.
        associatedLayer3VirtualNetworkName: Name of the associated layer 3 virtual network.
    """
    client = client_manager.get_client()
    if not client:
        return {"error": "Not connected. Use connect() first."}

    kwargs = {}
    params = {}
    if fabricId is not None:
        params["fabricId"] = fabricId
    if vlanName is not None:
        params["vlanName"] = vlanName
    if vlanId is not None:
        params["vlanId"] = vlanId
    if trafficType is not None:
        params["trafficType"] = trafficType
    if associatedLayer3VirtualNetworkName is not None:
        params["associatedLayer3VirtualNetworkName"] = associatedLayer3VirtualNetworkName
    if params:
        kwargs["params"] = params
    return await client.request("GET", "/dna/intent/api/v1/sda/layer2VirtualNetworks/count", **kwargs)


@agent.tool()
async def update_fabric_devices(request_body: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Update fabric devices

    Updates fabric devices based on user input.

    Args:
        request_body: The request body containing fabric device updates.
    """
    client = client_manager.get_client()
    if not client:
        return {"error": "Not connected. Use connect() first."}

    kwargs = {"json": request_body}
    return await client.request("PUT", "/dna/intent/api/v1/sda/fabricDevices", **kwargs)


@agent.tool()
async def get_fabric_devices(
    fabricId: str,
    networkDeviceId: Optional[str] = None,
    deviceRoles: Optional[str] = None,
    offset: Optional[int] = None,
    limit: Optional[int] = None,
) -> Optional[Dict[str, Any]]:
    """Get fabric devices

    Returns a list of fabric devices that match the provided query parameters.

    Args:
        fabricId: ID of the fabric this device belongs to.
        networkDeviceId: Network device ID of the fabric device.
        deviceRoles: Device roles of the fabric device.
        offset: Starting record for pagination.
        limit: Maximum number of records to return (max 500).
    """
    client = client_manager.get_client()
    if not client:
        return {"error": "Not connected. Use connect() first."}

    kwargs = {}
    params = {"fabricId": fabricId}
    if networkDeviceId is not None:
        params["networkDeviceId"] = networkDeviceId
    if deviceRoles is not None:
        params["deviceRoles"] = deviceRoles
    if offset is not None:
        params["offset"] = offset
    if limit is not None:
        params["limit"] = limit
    kwargs["params"] = params
    return await client.request("GET", "/dna/intent/api/v1/sda/fabricDevices", **kwargs)


@agent.tool()
async def add_fabric_zone(request_body: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Add fabric zone

    Adds a fabric zone based on user input.

    Args:
        request_body: The request body containing fabric zone information.
    """
    client = client_manager.get_client()
    if not client:
        return {"error": "Not connected. Use connect() first."}

    kwargs = {"json": request_body}
    return await client.request("POST", "/dna/intent/api/v1/sda/fabricZones", **kwargs)


@agent.tool()
async def get_fabric_zones(
    id: Optional[str] = None,
    siteId: Optional[str] = None,
    offset: Optional[int] = None,
    limit: Optional[int] = None,
) -> Optional[Dict[str, Any]]:
    """Get fabric zones

    Returns a list of fabric zones that match the provided query parameters.

    Args:
        id: ID of the fabric zone.
        siteId: ID of the network hierarchy associated with the fabric zone.
        offset: Starting record for pagination.
        limit: Maximum number of records to return (max 500).
    """
    client = client_manager.get_client()
    if not client:
        return {"error": "Not connected. Use connect() first."}

    kwargs = {}
    params = {}
    if id is not None:
        params["id"] = id
    if siteId is not None:
        params["siteId"] = siteId
    if offset is not None:
        params["offset"] = offset
    if limit is not None:
        params["limit"] = limit
    if params:
        kwargs["params"] = params
    return await client.request("GET", "/dna/intent/api/v1/sda/fabricZones", **kwargs)


@agent.tool()
async def update_fabric_zone(request_body: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Update fabric zone

    Updates a fabric zone based on user input.

    Args:
        request_body: The request body containing fabric zone updates.
    """
    client = client_manager.get_client()
    if not client:
        return {"error": "Not connected. Use connect() first."}

    kwargs = {"json": request_body}
    return await client.request("PUT", "/dna/intent/api/v1/sda/fabricZones", **kwargs)


@agent.tool()
async def add_fabric_site(request_body: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Add fabric site

    Adds a fabric site based on user input.

    Args:
        request_body: The request body containing fabric site information.
    """
    client = client_manager.get_client()
    if not client:
        return {"error": "Not connected. Use connect() first."}

    kwargs = {"json": request_body}
    return await client.request("POST", "/dna/intent/api/v1/sda/fabricSites", **kwargs)


@agent.tool()
async def update_fabric_site(request_body: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Update fabric site

    Updates a fabric site based on user input.

    Args:
        request_body: The request body containing fabric site updates.
    """
    client = client_manager.get_client()
    if not client:
        return {"error": "Not connected. Use connect() first."}

    kwargs = {"json": request_body}
    return await client.request("PUT", "/dna/intent/api/v1/sda/fabricSites", **kwargs)


@agent.tool()
async def get_fabric_sites(
    id: Optional[str] = None,
    siteId: Optional[str] = None,
    offset: Optional[int] = None,
    limit: Optional[int] = None,
) -> Optional[Dict[str, Any]]:
    """Get fabric sites

    Returns a list of fabric sites that match the provided query parameters.

    Args:
        id: ID of the fabric site.
        siteId: ID of the network hierarchy associated with the fabric site.
        offset: Starting record for pagination.
        limit: Maximum number of records to return (max 500).
    """
    client = client_manager.get_client()
    if not client:
        return {"error": "Not connected. Use connect() first."}

    kwargs = {}
    params = {}
    if id is not None:
        params["id"] = id
    if siteId is not None:
        params["siteId"] = siteId
    if offset is not None:
        params["offset"] = offset
    if limit is not None:
        params["limit"] = limit
    if params:
        kwargs["params"] = params
    return await client.request("GET", "/dna/intent/api/v1/sda/fabricSites", **kwargs)


@agent.tool()
async def get_layer3_virtual_networks_count(
    fabricId: Optional[str] = None, anchoredSiteId: Optional[str] = None
) -> Optional[Dict[str, Any]]:
    """Get layer 3 virtual networks count

    Returns the count of layer 3 virtual networks that match the provided query parameters.

    Args:
        fabricId: ID of the fabric the layer 3 virtual network is assigned to.
        anchoredSiteId: Fabric ID of the fabric site the layer 3 virtual network is anchored at.
    """
    client = client_manager.get_client()
    if not client:
        return {"error": "Not connected. Use connect() first."}

    kwargs = {}
    params = {}
    if fabricId is not None:
        params["fabricId"] = fabricId
    if anchoredSiteId is not None:
        params["anchoredSiteId"] = anchoredSiteId
    if params:
        kwargs["params"] = params
    return await client.request("GET", "/dna/intent/api/v1/sda/layer3VirtualNetworks/count", **kwargs)


@agent.tool()
async def get_fabric_devices_count(
    fabricId: str,
    networkDeviceId: Optional[str] = None,
    deviceRoles: Optional[str] = None,
) -> Optional[Dict[str, Any]]:
    """Get fabric devices count

    Returns the count of fabric devices that match the provided query parameters.

    Args:
        fabricId: ID of the fabric this device belongs to.
        networkDeviceId: Network device ID of the fabric device.
        deviceRoles: Device roles of the fabric device.
    """
    client = client_manager.get_client()
    if not client:
        return {"error": "Not connected. Use connect() first."}

    kwargs = {}
    params = {"fabricId": fabricId}
    if networkDeviceId is not None:
        params["networkDeviceId"] = networkDeviceId
    if deviceRoles is not None:
        params["deviceRoles"] = deviceRoles
    kwargs["params"] = params
    return await client.request("GET", "/dna/intent/api/v1/sda/fabricDevices/count", **kwargs)


@agent.tool()
async def read_list_of_virtual_networks_with_their_health_summary(
    x_caller_id: Optional[str] = None,
    startTime: Optional[float] = None,
    endTime: Optional[float] = None,
    limit: Optional[float] = None,
    offset: Optional[float] = None,
    sortBy: Optional[str] = None,
    order: Optional[str] = None,
    id: Optional[str] = None,
    vnLayer: Optional[str] = None,
    attribute: Optional[str] = None,
    view: Optional[str] = None,
    siteHierarchy: Optional[str] = None,
    SiteHierarchyId: Optional[str] = None,
) -> Optional[Dict[str, Any]]:
    """Read list of Virtual Networks with their health summary

    Get a paginated list of Virtual Networks with health summary.

    Args:
        x_caller_id: Optional caller ID to trace API calls.
        startTime: Start time for the data query in UNIX epoch milliseconds.
        endTime: End time for the data query in UNIX epoch milliseconds.
        limit: Maximum number of records to return.
        offset: Starting point for pagination (1-based).
        sortBy: A field within the response to sort by.
        order: The sort order of the field (ascending or descending).
        id: Comma-separated list of entity UUIDs to filter by.
        vnLayer: VN Layer information (Layer 3 or Layer 2 VNs).
        attribute: The interested fields in the request.
        view: The specific summary view being requested.
        siteHierarchy: Full site hierarchy path to filter by.
        SiteHierarchyId: Full site hierarchy UUID path to filter by.
    """
    client = client_manager.get_client()
    if not client:
        return {"error": "Not connected. Use connect() first."}

    kwargs = {}
    headers = {}
    if x_caller_id is not None:
        headers["X-CALLER-ID"] = x_caller_id
    if headers:
        kwargs["headers"] = headers

    params = {}
    if startTime is not None:
        params["startTime"] = startTime
    if endTime is not None:
        params["endTime"] = endTime
    if limit is not None:
        params["limit"] = limit
    if offset is not None:
        params["offset"] = offset
    if sortBy is not None:
        params["sortBy"] = sortBy
    if order is not None:
        params["order"] = order
    if id is not None:
        params["id"] = id
    if vnLayer is not None:
        params["vnLayer"] = vnLayer
    if attribute is not None:
        params["attribute"] = attribute
    if view is not None:
        params["view"] = view
    if siteHierarchy is not None:
        params["siteHierarchy"] = siteHierarchy
    if SiteHierarchyId is not None:
        params["SiteHierarchyId"] = SiteHierarchyId
    if params:
        kwargs["params"] = params
    return await client.request("GET", "/dna/data/api/v1/virtualNetworkHealthSummaries", **kwargs)


@agent.tool()
async def get_multicast(
    fabricId: Optional[str] = None,
    offset: Optional[int] = None,
    limit: Optional[int] = None,
) -> Optional[Dict[str, Any]]:
    """Get multicast

    Returns a list of multicast configurations at a fabric site level that match the provided query parameters.

    Args:
        fabricId: ID of the fabric site where multicast is configured.
        offset: Starting record for pagination.
        limit: Maximum number of records to return (max 500).
    """
    client = client_manager.get_client()
    if not client:
        return {"error": "Not connected. Use connect() first."}

    kwargs = {}
    params = {}
    if fabricId is not None:
        params["fabricId"] = fabricId
    if offset is not None:
        params["offset"] = offset
    if limit is not None:
        params["limit"] = limit
    if params:
        kwargs["params"] = params
    return await client.request("GET", "/dna/intent/api/v1/sda/multicast", **kwargs)


@agent.tool()
async def read_virtual_networks_count(
    x_caller_id: Optional[str] = None,
    startTime: Optional[float] = None,
    endTime: Optional[float] = None,
    id: Optional[str] = None,
    vnLayer: Optional[str] = None,
    siteHierarchy: Optional[str] = None,
    siteHierarchyId: Optional[str] = None,
) -> Optional[Dict[str, Any]]:
    """Read Virtual Networks count

    Get a count of virtual networks.

    Args:
        x_caller_id: Optional caller ID to trace API calls.
        startTime: Start time for the data query in UNIX epoch milliseconds.
        endTime: End time for the data query in UNIX epoch milliseconds.
        id: Comma-separated list of entity UUIDs to filter by.
        vnLayer: VN Layer information (Layer 3 or Layer 2 VNs).
        siteHierarchy: Full site hierarchy path to filter by.
        siteHierarchyId: Full site hierarchy UUID path to filter by.
    """
    client = client_manager.get_client()
    if not client:
        return {"error": "Not connected. Use connect() first."}

    kwargs = {}
    headers = {}
    if x_caller_id is not None:
        headers["X-CALLER-ID"] = x_caller_id
    if headers:
        kwargs["headers"] = headers

    params = {}
    if startTime is not None:
        params["startTime"] = startTime
    if endTime is not None:
        params["endTime"] = endTime
    if id is not None:
        params["id"] = id
    if vnLayer is not None:
        params["vnLayer"] = vnLayer
    if siteHierarchy is not None:
        params["siteHierarchy"] = siteHierarchy
    if siteHierarchyId is not None:
        params["siteHierarchyId"] = siteHierarchyId
    if params:
        kwargs["params"] = params
    return await client.request("GET", "/dna/data/api/v1/virtualNetworkHealthSummaries/count", **kwargs)


@agent.tool()
async def get_virtual_network_trend_analytics(
    id: str,
    trendInterval: str,
    x_caller_id: Optional[str] = None,
    startTime: Optional[float] = None,
    endTime: Optional[float] = None,
    limit: Optional[float] = None,
    offset: Optional[float] = None,
    order: Optional[str] = None,
    attribute: Optional[str] = None,
) -> Optional[Dict[str, Any]]:
    """The Trend analytics data for a virtual network in the specified time range

    Get health time series for a specific Virtual Network by providing its unique ID.

    Args:
        id: Unique virtual network ID.
        trendInterval: The time window to aggregate the metrics (e.g., '5 minutes', '1 hour').
        x_caller_id: Optional caller ID to trace API calls.
        startTime: Start time for the data query in UNIX epoch milliseconds.
        endTime: End time for the data query in UNIX epoch milliseconds.
        limit: Maximum number of records to return.
        offset: Starting point for pagination (1-based).
        order: The sort order of the field (ascending or descending).
        attribute: The interested fields in the request.
    """
    client = client_manager.get_client()
    if not client:
        return {"error": "Not connected. Use connect() first."}

    kwargs = {}
    headers = {}
    if x_caller_id is not None:
        headers["X-CALLER-ID"] = x_caller_id
    if headers:
        kwargs["headers"] = headers

    params = {"trendInterval": trendInterval}
    if startTime is not None:
        params["startTime"] = startTime
    if endTime is not None:
        params["endTime"] = endTime
    if limit is not None:
        params["limit"] = limit
    if offset is not None:
        params["offset"] = offset
    if order is not None:
        params["order"] = order
    if attribute is not None:
        params["attribute"] = attribute
    if params:
        kwargs["params"] = params
    return await client.request("GET", f"/dna/data/api/v1/virtualNetworkHealthSummaries/{id}/trendAnalytics", **kwargs)


@agent.tool()
async def get_port_assignments(
    fabricId: Optional[str] = None,
    networkDeviceId: Optional[str] = None,
    interfaceName: Optional[str] = None,
    dataVlanName: Optional[str] = None,
    voiceVlanName: Optional[str] = None,
    nativeVlanId: Optional[int] = None,
    offset: Optional[int] = None,
    limit: Optional[int] = None,
) -> Optional[Dict[str, Any]]:
    """Get port assignments

    Returns a list of port assignments that match the provided query parameters.

    Args:
        fabricId: ID of the fabric the device is assigned to.
        networkDeviceId: Network device ID of the port assignment.
        interfaceName: Interface name of the port assignment.
        dataVlanName: Data VLAN name of the port assignment.
        voiceVlanName: Voice VLAN name of the port assignment.
        nativeVlanId: Native VLAN of the port assignment (for TRUNKING_DEVICE type).
        offset: Starting record for pagination.
        limit: Maximum number of records to return (max 500).
    """
    client = client_manager.get_client()
    if not client:
        return {"error": "Not connected. Use connect() first."}

    kwargs = {}
    params = {}
    if fabricId is not None:
        params["fabricId"] = fabricId
    if networkDeviceId is not None:
        params["networkDeviceId"] = networkDeviceId
    if interfaceName is not None:
        params["interfaceName"] = interfaceName
    if dataVlanName is not None:
        params["dataVlanName"] = dataVlanName
    if voiceVlanName is not None:
        params["voiceVlanName"] = voiceVlanName
    if nativeVlanId is not None:
        params["nativeVlanId"] = nativeVlanId
    if offset is not None:
        params["offset"] = offset
    if limit is not None:
        params["limit"] = limit
    if params:
        kwargs["params"] = params
    return await client.request("GET", "/dna/intent/api/v1/sda/portAssignments", **kwargs)


@agent.tool()
async def add_port_assignments(request_body: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Add port assignments

    Adds port assignments based on user input.

    Args:
        request_body: The request body containing port assignment configurations.
    """
    client = client_manager.get_client()
    if not client:
        return {"error": "Not connected. Use connect() first."}

    kwargs = {"json": request_body}
    return await client.request("POST", "/dna/intent/api/v1/sda/portAssignments", **kwargs)


@agent.tool()
async def update_port_assignments(request_body: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Update port assignments

    Updates port assignments based on user input.

    Args:
        request_body: The request body containing port assignment updates.
    """
    client = client_manager.get_client()
    if not client:
        return {"error": "Not connected. Use connect() first."}

    kwargs = {"json": request_body}
    return await client.request("PUT", "/dna/intent/api/v1/sda/portAssignments", **kwargs)


@agent.tool()
async def read_fabric_site_count(
    x_caller_id: Optional[str] = None,
    startTime: Optional[float] = None,
    endTime: Optional[float] = None,
    id: Optional[str] = None,
    siteHierarchy: Optional[str] = None,
    siteHierarchyId: Optional[str] = None,
) -> Optional[Dict[str, Any]]:
    """Read fabric site count

    Get a count of Fabric sites.

    Args:
        x_caller_id: Optional caller ID to trace API calls.
        startTime: Start time for the data query in UNIX epoch milliseconds.
        endTime: End time for the data query in UNIX epoch milliseconds.
        id: Comma-separated list of entity UUIDs to filter by.
        siteHierarchy: Full site hierarchy path to filter by.
        siteHierarchyId: Full site hierarchy UUID path to filter by.
    """
    client = client_manager.get_client()
    if not client:
        return {"error": "Not connected. Use connect() first."}

    kwargs = {}
    headers = {}
    if x_caller_id is not None:
        headers["X-CALLER-ID"] = x_caller_id
    if headers:
        kwargs["headers"] = headers

    params = {}
    if startTime is not None:
        params["startTime"] = startTime
    if endTime is not None:
        params["endTime"] = endTime
    if id is not None:
        params["id"] = id
    if siteHierarchy is not None:
        params["siteHierarchy"] = siteHierarchy
    if siteHierarchyId is not None:
        params["siteHierarchyId"] = siteHierarchyId
    if params:
        kwargs["params"] = params
    return await client.request("GET", "/dna/data/api/v1/fabricSiteHealthSummaries/count", **kwargs)


@agent.tool()
async def get_anycast_gateway_count(
    fabricId: Optional[str] = None,
    virtualNetworkName: Optional[str] = None,
    ipPoolName: Optional[str] = None,
    vlanName: Optional[str] = None,
    vlanId: Optional[int] = None,
) -> Optional[Dict[str, Any]]:
    """Get anycast gateway count

    Returns the count of anycast gateways that match the provided query parameters.

    Args:
        fabricId: ID of the fabric the anycast gateway is assigned to.
        virtualNetworkName: Name of the virtual network associated with the anycast gateways.
        ipPoolName: Name of the IP pool associated with the anycast gateways.
        vlanName: VLAN name of the anycast gateways.
        vlanId: VLAN ID of the anycast gateways.
    """
    client = client_manager.get_client()
    if not client:
        return {"error": "Not connected. Use connect() first."}

    kwargs = {}
    params = {}
    if fabricId is not None:
        params["fabricId"] = fabricId
    if virtualNetworkName is not None:
        params["virtualNetworkName"] = virtualNetworkName
    if ipPoolName is not None:
        params["ipPoolName"] = ipPoolName
    if vlanName is not None:
        params["vlanName"] = vlanName
    if vlanId is not None:
        params["vlanId"] = vlanId
    if params:
        kwargs["params"] = params
    return await client.request("GET", "/dna/intent/api/v1/sda/anycastGateways/count", **kwargs)


@agent.tool()
async def get_provisioned_devices_count(siteId: Optional[str] = None) -> Optional[Dict[str, Any]]:
    """Get Provisioned Devices count

    Returns the count of provisioned devices based on query parameters.

    Args:
        siteId: ID of the site hierarchy.
    """
    client = client_manager.get_client()
    if not client:
        return {"error": "Not connected. Use connect() first."}

    kwargs = {}
    params = {}
    if siteId is not None:
        params["siteId"] = siteId
    if params:
        kwargs["params"] = params
    return await client.request("GET", "/dna/intent/api/v1/sda/provisionDevices/count", **kwargs)


@agent.tool()
async def add_extranet_policy(request_body: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """
    Add extranet policy.

    Args:
        request_body: The request body containing the extranet policy to add.
    """
    client = client_manager.get_client()
    if not client:
        return {"error": "Not connected. Use connect() first."}

    kwargs = {"json": request_body}
    return await client.request("POST", "/dna/intent/api/v1/sda/extranetPolicies", **kwargs)


@agent.tool()
async def add_fabric_devices(request_body: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """
    Add fabric devices.

    Args:
        request_body: The request body containing the fabric devices to add.
    """
    client = client_manager.get_client()
    if not client:
        return {"error": "Not connected. Use connect() first."}

    kwargs = {"json": request_body}
    return await client.request("POST", "/dna/intent/api/v1/sda/fabricDevices", **kwargs)


@agent.tool()
async def add_fabric_devices_layer2_handoffs(request_body: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """
    Add fabric devices layer 2 handoffs.

    Args:
        request_body: The request body containing the layer 2 handoff configurations.
    """
    client = client_manager.get_client()
    if not client:
        return {"error": "Not connected. Use connect() first."}

    kwargs = {"json": request_body}
    return await client.request("POST", "/dna/intent/api/v1/sda/fabricDevices/layer2Handoffs", **kwargs)


@agent.tool()
async def add_transit_networks(request_body: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """
    Add transit networks.

    Args:
        request_body: The request body containing the transit network configurations.
    """
    client = client_manager.get_client()
    if not client:
        return {"error": "Not connected. Use connect() first."}

    kwargs = {"json": request_body}
    return await client.request("POST", "/dna/intent/api/v1/sda/transitNetworks", **kwargs)


@agent.tool()
async def apply_pending_fabric_events(request_body: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """
    Apply pending fabric events.

    Args:
        request_body: The request body specifying which pending fabric events to apply.
    """
    client = client_manager.get_client()
    if not client:
        return {"error": "Not connected. Use connect() first."}

    kwargs = {"json": request_body}
    return await client.request("POST", "/dna/intent/api/v1/sda/pendingFabricEvents/apply", **kwargs)


@agent.tool()
async def delete_anycast_gateway_by_id(id: str) -> Optional[Dict[str, Any]]:
    """
    Delete anycast gateway by id.

    Args:
        id: ID of the anycast gateway to delete.
    """
    client = client_manager.get_client()
    if not client:
        return {"error": "Not connected. Use connect() first."}

    return await client.request("DELETE", f"/dna/intent/api/v1/sda/anycastGateways/{id}")


@agent.tool()
async def delete_extranet_policies(extranetPolicyName: Optional[str] = None) -> Optional[Dict[str, Any]]:
    """
    Delete extranet policies.

    Args:
        extranetPolicyName: Name of the extranet policy to delete.
    """
    client = client_manager.get_client()
    if not client:
        return {"error": "Not connected. Use connect() first."}

    kwargs = {}
    params = {}
    if extranetPolicyName is not None:
        params["extranetPolicyName"] = extranetPolicyName
    if params:
        kwargs["params"] = params
    return await client.request("DELETE", "/dna/intent/api/v1/sda/extranetPolicies", **kwargs)


@agent.tool()
async def delete_extranet_policy_by_id(id: str) -> Optional[Dict[str, Any]]:
    """
    Delete extranet policy by id.

    Args:
        id: ID of the extranet policy to delete.
    """
    client = client_manager.get_client()
    if not client:
        return {"error": "Not connected. Use connect() first."}

    return await client.request("DELETE", f"/dna/intent/api/v1/sda/extranetPolicies/{id}")


@agent.tool()
async def delete_fabric_device_by_id(id: str) -> Optional[Dict[str, Any]]:
    """
    Delete fabric device by id.

    Args:
        id: ID of the fabric device to delete.
    """
    client = client_manager.get_client()
    if not client:
        return {"error": "Not connected. Use connect() first."}

    return await client.request("DELETE", f"/dna/intent/api/v1/sda/fabricDevices/{id}")


@agent.tool()
async def delete_fabric_device_layer2_handoff_by_id(
    id: str,
) -> Optional[Dict[str, Any]]:
    """
    Delete fabric device layer 2 handoff by id.

    Args:
        id: ID of the layer 2 handoff of a fabric device.
    """
    client = client_manager.get_client()
    if not client:
        return {"error": "Not connected. Use connect() first."}

    return await client.request("DELETE", f"/dna/intent/api/v1/sda/fabricDevices/layer2Handoffs/{id}")


@agent.tool()
async def delete_fabric_device_layer2_handoffs(fabricId: str, networkDeviceId: str) -> Optional[Dict[str, Any]]:
    """
    Delete fabric device layer 2 handoffs.

    Args:
        fabricId: ID of the fabric this device belongs to.
        networkDeviceId: Network device ID of the fabric device.
    """
    client = client_manager.get_client()
    if not client:
        return {"error": "Not connected. Use connect() first."}

    kwargs = {}
    params = {"fabricId": fabricId, "networkDeviceId": networkDeviceId}
    kwargs["params"] = params
    return await client.request("DELETE", "/dna/intent/api/v1/sda/fabricDevices/layer2Handoffs", **kwargs)


@agent.tool()
async def delete_fabric_device_layer3_handoff_with_ip_transit_by_id(
    id: str,
) -> Optional[Dict[str, Any]]:
    """
    Delete fabric device layer 3 handoff with ip transit by id.

    Args:
        id: ID of the layer 3 handoff with ip transit of a fabric device.
    """
    client = client_manager.get_client()
    if not client:
        return {"error": "Not connected. Use connect() first."}

    return await client.request("DELETE", f"/dna/intent/api/v1/sda/fabricDevices/layer3Handoffs/ipTransits/{id}")


@agent.tool()
async def delete_fabric_devices(
    fabricId: str,
    networkDeviceId: Optional[str] = None,
    deviceRoles: Optional[str] = None,
) -> Optional[Dict[str, Any]]:
    """
    Delete fabric devices.

    Args:
        fabricId: ID of the fabric this device belongs to.
        networkDeviceId: Network device ID of the fabric device.
        deviceRoles: Device roles of the fabric device.
    """
    client = client_manager.get_client()
    if not client:
        return {"error": "Not connected. Use connect() first."}

    kwargs = {}
    params = {"fabricId": fabricId}
    if networkDeviceId is not None:
        params["networkDeviceId"] = networkDeviceId
    if deviceRoles is not None:
        params["deviceRoles"] = deviceRoles
    kwargs["params"] = params
    return await client.request("DELETE", "/dna/intent/api/v1/sda/fabricDevices", **kwargs)


@agent.tool()
async def delete_fabric_site_by_id(id: str) -> Optional[Dict[str, Any]]:
    """
    Delete fabric site by id.

    Args:
        id: ID of the fabric site to delete.
    """
    client = client_manager.get_client()
    if not client:
        return {"error": "Not connected. Use connect() first."}

    return await client.request("DELETE", f"/dna/intent/api/v1/sda/fabricSites/{id}")


@agent.tool()
async def delete_fabric_zone_by_id(id: str) -> Optional[Dict[str, Any]]:
    """
    Delete fabric zone by id.

    Args:
        id: ID of the fabric zone to delete.
    """
    client = client_manager.get_client()
    if not client:
        return {"error": "Not connected. Use connect() first."}

    return await client.request("DELETE", f"/dna/intent/api/v1/sda/fabricZones/{id}")


@agent.tool()
async def delete_layer2_virtual_network_by_id(id: str) -> Optional[Dict[str, Any]]:
    """
    Delete layer 2 virtual network by id.

    Args:
        id: ID of the layer 2 virtual network to delete.
    """
    client = client_manager.get_client()
    if not client:
        return {"error": "Not connected. Use connect() first."}

    return await client.request("DELETE", f"/dna/intent/api/v1/sda/layer2VirtualNetworks/{id}")


@agent.tool()
async def delete_layer3_virtual_network_by_id(id: str) -> Optional[Dict[str, Any]]:
    """
    Delete layer 3 virtual network by id.

    Args:
        id: ID of the layer 3 virtual network to delete.
    """
    client = client_manager.get_client()
    if not client:
        return {"error": "Not connected. Use connect() first."}

    return await client.request("DELETE", f"/dna/intent/api/v1/sda/layer3VirtualNetworks/{id}")


@agent.tool()
async def delete_port_assignment_by_id(id: str) -> Optional[Dict[str, Any]]:
    """
    Delete port assignment by id.

    Args:
        id: ID of the port assignment to delete.
    """
    client = client_manager.get_client()
    if not client:
        return {"error": "Not connected. Use connect() first."}

    return await client.request("DELETE", f"/dna/intent/api/v1/sda/portAssignments/{id}")


@agent.tool()
async def delete_port_assignments(
    fabricId: str,
    networkDeviceId: str,
    interfaceName: Optional[str] = None,
    dataVlanName: Optional[str] = None,
    voiceVlanName: Optional[str] = None,
) -> Optional[Dict[str, Any]]:
    """
    Delete port assignments.

    Args:
        fabricId: ID of the fabric the device is assigned to.
        networkDeviceId: Network device ID of the port assignment.
        interfaceName: Interface name of the port assignment.
        dataVlanName: Data VLAN name of the port assignment.
        voiceVlanName: Voice VLAN name of the port assignment.
    """
    client = client_manager.get_client()
    if not client:
        return {"error": "Not connected. Use connect() first."}

    kwargs = {}
    params = {"fabricId": fabricId, "networkDeviceId": networkDeviceId}
    if interfaceName is not None:
        params["interfaceName"] = interfaceName
    if dataVlanName is not None:
        params["dataVlanName"] = dataVlanName
    if voiceVlanName is not None:
        params["voiceVlanName"] = voiceVlanName
    kwargs["params"] = params
    return await client.request("DELETE", "/dna/intent/api/v1/sda/portAssignments", **kwargs)


@agent.tool()
async def delete_provisioned_device_by_id(id: str, cleanUpConfig: Optional[bool] = None) -> Optional[Dict[str, Any]]:
    """
    Delete provisioned device by Id.

    Args:
        id: ID of the provisioned device.
        cleanUpConfig: Enable/disable configuration cleanup for the device. Defaults to true.
    """
    client = client_manager.get_client()
    if not client:
        return {"error": "Not connected. Use connect() first."}

    kwargs = {}
    params = {}
    if cleanUpConfig is not None:
        params["cleanUpConfig"] = cleanUpConfig
    if params:
        kwargs["params"] = params
    return await client.request("DELETE", f"/dna/intent/api/v1/sda/provisionDevices/{id}", **kwargs)


@agent.tool()
async def delete_provisioned_devices(
    networkDeviceId: Optional[str] = None,
    siteId: Optional[str] = None,
    cleanUpConfig: Optional[bool] = None,
) -> Optional[Dict[str, Any]]:
    """
    Delete provisioned devices.

    Args:
        networkDeviceId: ID of the network device.
        siteId: ID of the site hierarchy.
        cleanUpConfig: Enable/disable configuration cleanup for the device(s). Defaults to true.
    """
    client = client_manager.get_client()
    if not client:
        return {"error": "Not connected. Use connect() first."}

    kwargs = {}
    params = {}
    if networkDeviceId is not None:
        params["networkDeviceId"] = networkDeviceId
    if siteId is not None:
        params["siteId"] = siteId
    if cleanUpConfig is not None:
        params["cleanUpConfig"] = cleanUpConfig
    if params:
        kwargs["params"] = params
    return await client.request("DELETE", "/dna/intent/api/v1/sda/provisionDevices", **kwargs)


@agent.tool()
async def delete_transit_network_by_id(id: str) -> Optional[Dict[str, Any]]:
    """
    Delete transit network by id.

    Args:
        id: ID of the transit network to delete.
    """
    client = client_manager.get_client()
    if not client:
        return {"error": "Not connected. Use connect() first."}

    return await client.request("DELETE", f"/dna/intent/api/v1/sda/transitNetworks/{id}")


@agent.tool()
async def get_authentication_profiles(
    fabricId: Optional[str] = None,
    authenticationProfileName: Optional[str] = None,
    isGlobalAuthenticationProfile: Optional[bool] = None,
    offset: Optional[float] = None,
    limit: Optional[float] = None,
) -> Optional[Dict[str, Any]]:
    """
    Get authentication profiles.

    Args:
        fabricId: ID of the fabric the authentication profile is assigned to.
        authenticationProfileName: Return only profiles with this name.
        isGlobalAuthenticationProfile: Set to true for global profiles, false to hide them.
        offset: Starting record for pagination.
        limit: Maximum number of records to return (max 500).
    """
    client = client_manager.get_client()
    if not client:
        return {"error": "Not connected. Use connect() first."}

    kwargs = {}
    params = {}
    if fabricId is not None:
        params["fabricId"] = fabricId
    if authenticationProfileName is not None:
        params["authenticationProfileName"] = authenticationProfileName
    if isGlobalAuthenticationProfile is not None:
        params["isGlobalAuthenticationProfile"] = isGlobalAuthenticationProfile
    if offset is not None:
        params["offset"] = offset
    if limit is not None:
        params["limit"] = limit
    if params:
        kwargs["params"] = params
    return await client.request("GET", "/dna/intent/api/v1/sda/authenticationProfiles", **kwargs)


@agent.tool()
async def get_extranet_policies(
    extranetPolicyName: Optional[str] = None,
    offset: Optional[float] = None,
    limit: Optional[float] = None,
) -> Optional[Dict[str, Any]]:
    """
    Get extranet policies.

    Args:
        extranetPolicyName: Name of the extranet policy.
        offset: Starting record for pagination.
        limit: Maximum number of records to return (max 500).
    """
    client = client_manager.get_client()
    if not client:
        return {"error": "Not connected. Use connect() first."}

    kwargs = {}
    params = {}
    if extranetPolicyName is not None:
        params["extranetPolicyName"] = extranetPolicyName
    if offset is not None:
        params["offset"] = offset
    if limit is not None:
        params["limit"] = limit
    if params:
        kwargs["params"] = params
    return await client.request("GET", "/dna/intent/api/v1/sda/extranetPolicies", **kwargs)


@agent.tool()
async def get_fabric_devices_layer2_handoffs(
    fabricId: str,
    networkDeviceId: Optional[str] = None,
    offset: Optional[float] = None,
    limit: Optional[float] = None,
) -> Optional[Dict[str, Any]]:
    """
    Get fabric devices layer 2 handoffs.

    Args:
        fabricId: ID of the fabric this device belongs to.
        networkDeviceId: Network device ID of the fabric device.
        offset: Starting record for pagination.
        limit: Maximum number of records to return (max 500).
    """
    client = client_manager.get_client()
    if not client:
        return {"error": "Not connected. Use connect() first."}

    kwargs = {}
    params = {"fabricId": fabricId}
    if networkDeviceId is not None:
        params["networkDeviceId"] = networkDeviceId
    if offset is not None:
        params["offset"] = offset
    if limit is not None:
        params["limit"] = limit
    kwargs["params"] = params
    return await client.request("GET", "/dna/intent/api/v1/sda/fabricDevices/layer2Handoffs", **kwargs)


@agent.tool()
async def get_fabric_devices_layer3_handoffs_with_ip_transit_count(
    fabricId: str, networkDeviceId: Optional[str] = None
) -> Optional[Dict[str, Any]]:
    """
    Get fabric devices layer 3 handoffs with ip transit count.

    Args:
        fabricId: ID of the fabric this device belongs to.
        networkDeviceId: Network device ID of the fabric device.
    """
    client = client_manager.get_client()
    if not client:
        return {"error": "Not connected. Use connect() first."}

    kwargs = {}
    params = {"fabricId": fabricId}
    if networkDeviceId is not None:
        params["networkDeviceId"] = networkDeviceId
    kwargs["params"] = params
    return await client.request(
        "GET",
        "/dna/intent/api/v1/sda/fabricDevices/layer3Handoffs/ipTransits/count",
        **kwargs,
    )


@agent.tool()
async def get_fabric_devices_layer3_handoffs_with_sda_transit_count(
    fabricId: str, networkDeviceId: Optional[str] = None
) -> Optional[Dict[str, Any]]:
    """
    Get fabric devices layer 3 handoffs with sda transit count.

    Args:
        fabricId: ID of the fabric this device belongs to.
        networkDeviceId: Network device ID of the fabric device.
    """
    client = client_manager.get_client()
    if not client:
        return {"error": "Not connected. Use connect() first."}

    kwargs = {}
    params = {"fabricId": fabricId}
    if networkDeviceId is not None:
        params["networkDeviceId"] = networkDeviceId
    kwargs["params"] = params
    return await client.request(
        "GET",
        "/dna/intent/api/v1/sda/fabricDevices/layer3Handoffs/sdaTransits/count",
        **kwargs,
    )


@agent.tool()
async def get_multicast_virtual_network_count(
    fabricId: Optional[str] = None,
) -> Optional[Dict[str, Any]]:
    """
    Get multicast virtual network count.

    Args:
        fabricId: ID of the fabric site the multicast configuration is associated with.
    """
    client = client_manager.get_client()
    if not client:
        return {"error": "Not connected. Use connect() first."}

    kwargs = {}
    params = {}
    if fabricId is not None:
        params["fabricId"] = fabricId
    if params:
        kwargs["params"] = params
    return await client.request("GET", "/dna/intent/api/v1/sda/multicast/virtualNetworks/count", **kwargs)


@agent.tool()
async def get_port_channel_count(
    fabricId: Optional[str] = None,
    networkDeviceId: Optional[str] = None,
    portChannelName: Optional[str] = None,
    connectedDeviceType: Optional[str] = None,
) -> Optional[Dict[str, Any]]:
    """
    Get port channel count.

    Args:
        fabricId: ID of the fabric the device is assigned to.
        networkDeviceId: ID of the network device.
        portChannelName: Name of the port channel.
        connectedDeviceType: Connected device type of the port channel (TRUNK or EXTENDED_NODE).
    """
    client = client_manager.get_client()
    if not client:
        return {"error": "Not connected. Use connect() first."}

    kwargs = {}
    params = {}
    if fabricId is not None:
        params["fabricId"] = fabricId
    if networkDeviceId is not None:
        params["networkDeviceId"] = networkDeviceId
    if portChannelName is not None:
        params["portChannelName"] = portChannelName
    if connectedDeviceType is not None:
        params["connectedDeviceType"] = connectedDeviceType
    if params:
        kwargs["params"] = params
    return await client.request("GET", "/dna/intent/api/v1/sda/portChannels/count", **kwargs)


@agent.tool()
async def get_transit_networks(
    id: Optional[str] = None,
    name: Optional[str] = None,
    type: Optional[str] = None,
    offset: Optional[float] = None,
    limit: Optional[float] = None,
) -> Optional[Dict[str, Any]]:
    """
    Get transit networks.

    Args:
        id: ID of the transit network.
        name: Name of the transit network.
        type: Type of the transit network (e.g., IP_BASED_TRANSIT).
        offset: Starting record for pagination.
        limit: Maximum number of records to return (max 500).
    """
    client = client_manager.get_client()
    if not client:
        return {"error": "Not connected. Use connect() first."}

    kwargs = {}
    params = {}
    if id is not None:
        params["id"] = id
    if name is not None:
        params["name"] = name
    if type is not None:
        params["type"] = type
    if offset is not None:
        params["offset"] = offset
    if limit is not None:
        params["limit"] = limit
    if params:
        kwargs["params"] = params
    return await client.request("GET", "/dna/intent/api/v1/sda/transitNetworks", **kwargs)


@agent.tool()
async def get_transit_networks_count(
    type: Optional[str] = None,
) -> Optional[Dict[str, Any]]:
    """
    Get transit networks count.

    Args:
        type: Type of the transit network (e.g., IP_BASED_TRANSIT).
    """
    client = client_manager.get_client()
    if not client:
        return {"error": "Not connected. Use connect() first."}

    kwargs = {}
    params = {}
    if type is not None:
        params["type"] = type
    if params:
        kwargs["params"] = params
    return await client.request("GET", "/dna/intent/api/v1/sda/transitNetworks/count", **kwargs)


@agent.tool()
async def read_fabric_entity_summary(
    x_caller_id: Optional[str] = None,
    startTime: Optional[float] = None,
    endTime: Optional[float] = None,
    siteHierarchy: Optional[str] = None,
    siteHierarchyId: Optional[str] = None,
) -> Optional[Dict[str, Any]]:
    """
    Read Fabric entity summary.

    Args:
        x_caller_id: Optional caller ID to trace API calls.
        startTime: Start time for the data query in UNIX epoch milliseconds.
        endTime: End time for the data query in UNIX epoch milliseconds.
        siteHierarchy: Full site hierarchy path to filter by.
        siteHierarchyId: Full site hierarchy UUID path to filter by.
    """
    client = client_manager.get_client()
    if not client:
        return {"error": "Not connected. Use connect() first."}

    kwargs = {}
    headers = {}
    if x_caller_id is not None:
        headers["X-CALLER-ID"] = x_caller_id
    if headers:
        kwargs["headers"] = headers

    params = {}
    if startTime is not None:
        params["startTime"] = startTime
    if endTime is not None:
        params["endTime"] = endTime
    if siteHierarchy is not None:
        params["siteHierarchy"] = siteHierarchy
    if siteHierarchyId is not None:
        params["siteHierarchyId"] = siteHierarchyId
    if params:
        kwargs["params"] = params
    return await client.request("GET", "/dna/data/api/v1/fabricSummary", **kwargs)


@agent.tool()
async def read_fabric_sites_with_health_summary_from_id(
    id: str,
    x_caller_id: Optional[str] = None,
    startTime: Optional[float] = None,
    endTime: Optional[float] = None,
    attribute: Optional[str] = None,
    view: Optional[str] = None,
) -> Optional[Dict[str, Any]]:
    """
    Read Fabric Sites with health summary from id.

    Args:
        id: Unique fabric site id.
        x_caller_id: Optional caller ID to trace API calls.
        startTime: Start time for the data query in UNIX epoch milliseconds.
        endTime: End time for the data query in UNIX epoch milliseconds.
        attribute: List of FabricSite health attributes to include.
        view: The specific summary view being requested.
    """
    client = client_manager.get_client()
    if not client:
        return {"error": "Not connected. Use connect() first."}

    kwargs = {}
    headers = {}
    if x_caller_id is not None:
        headers["X-CALLER-ID"] = x_caller_id
    if headers:
        kwargs["headers"] = headers

    params = {}
    if startTime is not None:
        params["startTime"] = startTime
    if endTime is not None:
        params["endTime"] = endTime
    if attribute is not None:
        params["attribute"] = attribute
    if view is not None:
        params["view"] = view
    if params:
        kwargs["params"] = params
    return await client.request("GET", f"/dna/data/api/v1/fabricSiteHealthSummaries/{id}", **kwargs)


@agent.tool()
async def read_transit_networks_count(
    x_caller_id: Optional[str] = None,
    startTime: Optional[float] = None,
    endTime: Optional[float] = None,
    id: Optional[str] = None,
) -> Optional[Dict[str, Any]]:
    """
    Read Transit Networks count.

    Args:
        x_caller_id: Optional caller ID to trace API calls.
        startTime: Start time for the data query in UNIX epoch milliseconds.
        endTime: End time for the data query in UNIX epoch milliseconds.
        id: Comma-separated list of transit entity IDs to filter by.
    """
    client = client_manager.get_client()
    if not client:
        return {"error": "Not connected. Use connect() first."}

    kwargs = {}
    headers = {}
    if x_caller_id is not None:
        headers["X-CALLER-ID"] = x_caller_id
    if headers:
        kwargs["headers"] = headers

    params = {}
    if startTime is not None:
        params["startTime"] = startTime
    if endTime is not None:
        params["endTime"] = endTime
    if id is not None:
        params["id"] = id
    if params:
        kwargs["params"] = params
    return await client.request("GET", "/dna/data/api/v1/transitNetworkHealthSummaries/count", **kwargs)


@agent.tool()
async def the_trend_analytics_data_for_a_fabric_site_in_the_specified_time_range(
    id: str,
    trendInterval: str,
    x_caller_id: Optional[str] = None,
    startTime: Optional[float] = None,
    endTime: Optional[float] = None,
    limit: Optional[float] = None,
    offset: Optional[float] = None,
    order: Optional[str] = None,
    attribute: Optional[str] = None,
) -> Optional[Dict[str, Any]]:
    """
    Get the Trend analytics data for a fabric site in the specified time range.

    Args:
        id: Unique fabric site id.
        trendInterval: The time window to aggregate the metrics (e.g., '5 minutes', '1 hour').
        x_caller_id: Optional caller ID to trace API calls.
        startTime: Start time for the data query in UNIX epoch milliseconds.
        endTime: End time for the data query in UNIX epoch milliseconds.
        limit: Maximum number of records to return.
        offset: Starting point for pagination (1-based).
        order: The sort order of the field (ascending or descending).
        attribute: The interested fields in the request.
    """
    client = client_manager.get_client()
    if not client:
        return {"error": "Not connected. Use connect() first."}

    kwargs = {}
    headers = {}
    if x_caller_id is not None:
        headers["X-CALLER-ID"] = x_caller_id
    if headers:
        kwargs["headers"] = headers

    params = {"trendInterval": trendInterval}
    if startTime is not None:
        params["startTime"] = startTime
    if endTime is not None:
        params["endTime"] = endTime
    if limit is not None:
        params["limit"] = limit
    if offset is not None:
        params["offset"] = offset
    if order is not None:
        params["order"] = order
    if attribute is not None:
        params["attribute"] = attribute
    if params:
        kwargs["params"] = params
    return await client.request("GET", f"/dna/data/api/v1/fabricSiteHealthSummaries/{id}/trendAnalytics", **kwargs)


@agent.tool()
async def the_trend_analytics_data_for_a_virtual_network_in_the_specified_time_range(
    id: str,
    trendInterval: str,
    x_caller_id: Optional[str] = None,
    startTime: Optional[float] = None,
    endTime: Optional[float] = None,
    limit: Optional[float] = None,
    offset: Optional[float] = None,
    order: Optional[str] = None,
    attribute: Optional[str] = None,
) -> Optional[Dict[str, Any]]:
    """
    Get the Trend analytics data for a virtual network in the specified time range.

    Args:
        id: Unique virtual network id.
        trendInterval: The time window to aggregate the metrics (e.g., '5 minutes', '1 hour').
        x_caller_id: Optional caller ID to trace API calls.
        startTime: Start time for the data query in UNIX epoch milliseconds.
        endTime: End time for the data query in UNIX epoch milliseconds.
        limit: Maximum number of records to return.
        offset: Starting point for pagination (1-based).
        order: The sort order of the field (ascending or descending).
        attribute: The interested fields in the request.
    """
    client = client_manager.get_client()
    if not client:
        return {"error": "Not connected. Use connect() first."}

    kwargs = {}
    headers = {}
    if x_caller_id is not None:
        headers["X-CALLER-ID"] = x_caller_id
    if headers:
        kwargs["headers"] = headers

    params = {"trendInterval": trendInterval}
    if startTime is not None:
        params["startTime"] = startTime
    if endTime is not None:
        params["endTime"] = endTime
    if limit is not None:
        params["limit"] = limit
    if offset is not None:
        params["offset"] = offset
    if order is not None:
        params["order"] = order
    if attribute is not None:
        params["attribute"] = attribute
    if params:
        kwargs["params"] = params
    return await client.request("GET", f"/dna/data/api/v1/virtualNetworkHealthSummaries/{id}/trendAnalytics", **kwargs)


@agent.tool()
async def update_authentication_profile(request_body: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """
    Update authentication profile.

    Args:
        request_body: The request body containing the authentication profile updates.
    """
    client = client_manager.get_client()
    if not client:
        return {"error": "Not connected. Use connect() first."}

    kwargs = {"json": request_body}
    return await client.request("PUT", "/dna/intent/api/v1/sda/authenticationProfiles", **kwargs)


@agent.tool()
async def update_extranet_policy(request_body: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """
    Update extranet policy.

    Args:
        request_body: The request body containing the extranet policy updates.
    """
    client = client_manager.get_client()
    if not client:
        return {"error": "Not connected. Use connect() first."}

    kwargs = {"json": request_body}
    return await client.request("PUT", "/dna/intent/api/v1/sda/extranetPolicies", **kwargs)


@agent.tool()
async def update_multicast(request_body: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """
    Update multicast.

    Args:
        request_body: The request body containing the multicast configuration updates.
    """
    client = client_manager.get_client()
    if not client:
        return {"error": "Not connected. Use connect() first."}

    kwargs = {"json": request_body}
    return await client.request("PUT", "/dna/intent/api/v1/sda/multicast", **kwargs)


@agent.tool()
async def update_transit_networks(request_body: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """
    Update transit networks.

    Args:
        request_body: The request body containing the transit network updates.
    """
    client = client_manager.get_client()
    if not client:
        return {"error": "Not connected. Use connect() first."}

    kwargs = {"json": request_body}
    return await client.request("PUT", "/dna/intent/api/v1/sda/transitNetworks", **kwargs)


# Register all tools with the smart agent
def register_sda_tools():
    """Register all SDA tools with the smart domain agent."""
    tools_to_register = [
        connect, get_edge_device_from_sda_fabric, get_device_info_from_sda_fabric,
        add_ip_pool_in_sda_virtual_network, delete_ip_pool_from_sda_virtual_network,
        get_ip_pool_from_sda_virtual_network, get_site_from_sda_fabric,
        add_site_in_sda_fabric, get_multicast_details_from_sda_fabric,
        add_vn_in_fabric, get_vn_from_sda_fabric, delete_vn_from_sda_fabric,
        get_sites, get_network_devices, get_multicast_virtual_networks,
        # Add more tools as needed
    ]
    
    for tool_func in tools_to_register:
        smart_agent.register_tool(tool_func.__name__, tool_func)


# Process request method for the SDA agent
async def process_request(query: str) -> str:
    """
    Process SDA-related requests with intelligent routing.
    """
    return await smart_agent.process_request(query)

# Call registration on module load
register_sda_tools()

# Expose process_request at module level for router access
agent.process_request = process_request
