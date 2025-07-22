import urllib.parse
from typing import Any, List, Dict, Optional
import httpx
import base64
import json
import os
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("CatC-MCP")

# Constants
AUTH_TIMEOUT = 60.0
REQUEST_TIMEOUT = 30.0


class CatalystCenterClient:
    """Client for interacting with Cisco Catalyst Center API."""

    def __init__(self, base_url: str = None, username: str = None, password: str = None):
        self.base_url = base_url
        self.username = username
        self.password = password
        self.token = None

    async def authenticate(self) -> bool:
        """Authenticate and get token from Catalyst Center."""
        auth_url = f"{self.base_url}/dna/system/api/v1/auth/token"
        auth_string = f"{self.username}:{self.password}"
        encoded_auth = base64.b64encode(auth_string.encode()).decode()

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Basic {encoded_auth}"
        }

        async with httpx.AsyncClient(verify=False) as client:
            try:
                response = await client.post(auth_url, headers=headers, timeout=AUTH_TIMEOUT)
                response.raise_for_status()
                self.token = response.json().get("Token")
                return bool(self.token)
            except Exception as e:
                print(f"Authentication error: {str(e)}")
                return False

    async def request(self, method: str, endpoint: str, **kwargs) -> Optional[Dict[str, Any]]:
        """Make an API request to Catalyst Center with authentication."""
        if not self.token and not await self.authenticate():
            return None

        url = f"{self.base_url}{endpoint}"
        headers = {
            "Content-Type": "application/json",
            "X-Auth-Token": self.token
        }

        if "headers" in kwargs:
            kwargs["headers"].update(headers)
        else:
            kwargs["headers"] = headers

        kwargs["timeout"] = kwargs.get("timeout", REQUEST_TIMEOUT)

        async with httpx.AsyncClient(verify=False) as client:
            try:
                response = await getattr(client, method.lower())(url, **kwargs)
                response.raise_for_status()
                return response.json()
            except httpx.HTTPStatusError as e:
                if e.response.status_code == 401:
                    # Token expired, try to re-authenticate
                    if await self.authenticate():
                        # Update headers with new token and retry
                        if "headers" in kwargs:
                            kwargs["headers"]["X-Auth-Token"] = self.token
                        return await self.request(method, endpoint, **kwargs)
                print(f"API error: {str(e)}")
                return None
            except Exception as e:
                print(f"Request error: {str(e)}")
                return None


# Client instance
client = None


@mcp.tool()
async def connect(base_url: str, username: str, password: str) -> str:
    """Connect to Cisco Catalyst Center.

    Args:
        base_url: Base URL of the Catalyst Center (e.g., https://10.10.10.10)
        username: Username for authentication
        password: Password for authentication
    """
    global client
    client = CatalystCenterClient(base_url, username, password)
    if await client.authenticate():
        return "Successfully connected to Cisco Catalyst Center"
    return "Failed to connect to Cisco Catalyst Center"


@mcp.tool()
async def get_fabric_devices_layer2_handoffs_count(fabricId: str, networkDeviceId: Optional[str] = None) -> Optional[Dict[str, Any]]:
    """Get fabric devices layer 2 handoffs count

    Returns the count of layer 2 handoffs of fabric devices that match the provided query parameters.

    Args:
        fabricId: ID of the fabric this device belongs to.
        networkDeviceId: Network device ID of the fabric device.
    """
    global client
    if not client:
        return {"error": "Not connected. Use connect() first."}

    kwargs = {}
    params = {}
    if fabricId is not None:
        params['fabricId'] = fabricId
    if networkDeviceId is not None:
        params['networkDeviceId'] = networkDeviceId
    if params:
        kwargs['params'] = params
    return await client.request('GET', f'/dna/intent/api/v1/sda/fabricDevices/layer2Handoffs/count', **kwargs)

@mcp.tool()
async def sda_fabric_sites_readiness(order: Optional[int] = None, sortBy: Optional[str] = None) -> Optional[Dict[str, Any]]:
    """Sda Fabric Sites Readiness

    Gets a list of all SDA fabric sites along with their readiness status for Security Service Insertion (SSI) deployment.

    Args:
        order: Whether ascending or descending order should be used to sort the response.
        sortBy: Sort results by the fabric site name.
    """
    global client
    if not client:
        return {"error": "Not connected. Use connect() first."}

    kwargs = {}
    params = {}
    if order is not None:
        params['order'] = order
    if sortBy is not None:
        params['sortBy'] = sortBy
    if params:
        kwargs['params'] = params
    return await client.request('GET', f'/dna/intent/api/v1/securityServiceInsertion/fabricSitesReadiness', **kwargs)

@mcp.tool()
async def get_fabric_site_count() -> Optional[Dict[str, Any]]:
    """Get fabric site count

    Returns the count of fabric sites that match the provided query parameters.

    """
    global client
    if not client:
        return {"error": "Not connected. Use connect() first."}

    kwargs = {}
    return await client.request('GET', f'/dna/intent/api/v1/sda/fabricSites/count', **kwargs)


@mcp.tool()
async def get_anycast_gateways(id: Optional[str] = None, fabricId: Optional[str] = None, virtualNetworkName: Optional[str] = None, ipPoolName: Optional[str] = None, vlanName: Optional[str] = None, vlanId: Optional[int] = None, offset: Optional[int] = None, limit: Optional[int] = None) -> Optional[Dict[str, Any]]:
    """Get anycast gateways

    Returns a list of anycast gateways that match the provided query parameters.

    Args:
        id: ID of the anycast gateway.
        fabricId: ID of the fabric the anycast gateway is assigned to.
        virtualNetworkName: Name of the virtual network associated with the anycast gateways.
        ipPoolName: Name of the IP pool associated with the anycast gateways.
        vlanName: VLAN name of the anycast gateways.
        vlanId: VLAN ID of the anycast gateways. The allowed range for vlanId is [2-4093] except for reserved VLANs [1002-1005], 2046, and 4094.
        offset: Starting record for pagination.
        limit: Maximum number of records to return. The maximum number of objects supported in a single request is 500.
    """
    global client
    if not client:
        return {"error": "Not connected. Use connect() first."}

    kwargs = {}
    params = {}
    if id is not None:
        params['id'] = id
    if fabricId is not None:
        params['fabricId'] = fabricId
    if virtualNetworkName is not None:
        params['virtualNetworkName'] = virtualNetworkName
    if ipPoolName is not None:
        params['ipPoolName'] = ipPoolName
    if vlanName is not None:
        params['vlanName'] = vlanName
    if vlanId is not None:
        params['vlanId'] = vlanId
    if offset is not None:
        params['offset'] = offset
    if limit is not None:
        params['limit'] = limit
    if params:
        kwargs['params'] = params
    return await client.request('GET', f'/dna/intent/api/v1/sda/anycastGateways', **kwargs)

@mcp.tool()
async def add_anycast_gateways(request_body: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Add anycast gateways

    Adds anycast gateways based on user input.

    Args:
        request_body: Request body data
    """
    global client
    if not client:
        return {"error": "Not connected. Use connect() first."}

    kwargs = {}
    kwargs['json'] = request_body
    return await client.request('POST', f'/dna/intent/api/v1/sda/anycastGateways', **kwargs)


@mcp.tool()
async def get_fabric_zone_count() -> Optional[Dict[str, Any]]:
    """Get fabric zone count

    Returns the count of fabric zones that match the provided query parameters.

    """
    global client
    if not client:
        return {"error": "Not connected. Use connect() first."}

    kwargs = {}
    return await client.request('GET', f'/dna/intent/api/v1/sda/fabricZones/count', **kwargs)


@mcp.tool()
async def update_layer2_virtual_networks(request_body: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Update layer 2 virtual networks

    Updates layer 2 virtual networks based on user input.

    Args:
        request_body: Request body data
    """
    global client
    if not client:
        return {"error": "Not connected. Use connect() first."}

    kwargs = {}
    kwargs['json'] = request_body
    return await client.request('PUT', f'/dna/intent/api/v1/sda/layer2VirtualNetworks', **kwargs)

@mcp.tool()
async def get_layer2_virtual_networks(id: Optional[str] = None, fabricId: Optional[str] = None, vlanName: Optional[str] = None, vlanId: Optional[int] = None, trafficType: Optional[str] = None, associatedLayer3VirtualNetworkName: Optional[str] = None, offset: Optional[int] = None, limit: Optional[int] = None) -> Optional[Dict[str, Any]]:
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
        limit: Maximum number of records to return. The maximum number of objects supported in a single request is 500.
    """
    global client
    if not client:
        return {"error": "Not connected. Use connect() first."}

    kwargs = {}
    params = {}
    if id is not None:
        params['id'] = id
    if fabricId is not None:
        params['fabricId'] = fabricId
    if vlanName is not None:
        params['vlanName'] = vlanName
    if vlanId is not None:
        params['vlanId'] = vlanId
    if trafficType is not None:
        params['trafficType'] = trafficType
    if associatedLayer3VirtualNetworkName is not None:
        params['associatedLayer3VirtualNetworkName'] = associatedLayer3VirtualNetworkName
    if offset is not None:
        params['offset'] = offset
    if limit is not None:
        params['limit'] = limit
    if params:
        kwargs['params'] = params
    return await client.request('GET', f'/dna/intent/api/v1/sda/layer2VirtualNetworks', **kwargs)

@mcp.tool()
async def delete_layer2_virtual_networks(fabricId: str, vlanName: Optional[str] = None, vlanId: Optional[int] = None, trafficType: Optional[str] = None, associatedLayer3VirtualNetworkName: Optional[str] = None) -> Optional[Dict[str, Any]]:
    """Delete layer 2 virtual networks

    Deletes layer 2 virtual networks based on user input.

    Args:
        fabricId: ID of the fabric the layer 2 virtual network is assigned to.
        vlanName: The vlan name of the layer 2 virtual network.
        vlanId: The vlan ID of the layer 2 virtual network.
        trafficType: The traffic type of the layer 2 virtual network.
        associatedLayer3VirtualNetworkName: Name of the associated layer 3 virtual network.
    """
    global client
    if not client:
        return {"error": "Not connected. Use connect() first."}

    kwargs = {}
    params = {}
    if fabricId is not None:
        params['fabricId'] = fabricId
    if vlanName is not None:
        params['vlanName'] = vlanName
    if vlanId is not None:
        params['vlanId'] = vlanId
    if trafficType is not None:
        params['trafficType'] = trafficType
    if associatedLayer3VirtualNetworkName is not None:
        params['associatedLayer3VirtualNetworkName'] = associatedLayer3VirtualNetworkName
    if params:
        kwargs['params'] = params
    return await client.request('DELETE', f'/dna/intent/api/v1/sda/layer2VirtualNetworks', **kwargs)

@mcp.tool()
async def add_layer2_virtual_networks(request_body: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Add layer 2 virtual networks

    Adds layer 2 virtual networks based on user input.

    Args:
        request_body: Request body data
    """
    global client
    if not client:
        return {"error": "Not connected. Use connect() first."}

    kwargs = {}
    kwargs['json'] = request_body
    return await client.request('POST', f'/dna/intent/api/v1/sda/layer2VirtualNetworks', **kwargs)


@mcp.tool()
async def get_fabric_devices_layer3_handoffs_with_sda_transit(fabricId: str, networkDeviceId: Optional[str] = None, offset: Optional[int] = None, limit: Optional[int] = None) -> Optional[Dict[str, Any]]:
    """Get fabric devices layer 3 handoffs with sda transit

    Returns a list of layer 3 handoffs with sda transit of fabric devices that match the provided query parameters.

    Args:
        fabricId: ID of the fabric this device belongs to.
        networkDeviceId: Network device ID of the fabric device.
        offset: Starting record for pagination.
        limit: Maximum number of records to return. The maximum number of objects supported in a single request is 500.
    """
    global client
    if not client:
        return {"error": "Not connected. Use connect() first."}

    kwargs = {}
    params = {}
    if fabricId is not None:
        params['fabricId'] = fabricId
    if networkDeviceId is not None:
        params['networkDeviceId'] = networkDeviceId
    if offset is not None:
        params['offset'] = offset
    if limit is not None:
        params['limit'] = limit
    if params:
        kwargs['params'] = params
    return await client.request('GET', f'/dna/intent/api/v1/sda/fabricDevices/layer3Handoffs/sdaTransits', **kwargs)


@mcp.tool()
async def read_list_of_fabric_sites_with_their_health_summary(startTime: Optional[int] = None, endTime: Optional[int] = None, limit: Optional[int] = None, offset: Optional[int] = None, sortBy: Optional[str] = None, order: Optional[str] = None, id: Optional[str] = None, attribute: Optional[str] = None, view: Optional[str] = None, siteHierarchy: Optional[str] = None, siteHierarchyId: Optional[str] = None) -> Optional[Dict[str, Any]]:
    """Read list of Fabric Sites with their health summary

    Get a paginated list of Fabric sites Networks with health summary.

This API provides the latest health data until the given `endTime`. If data is not ready for the provided endTime, the request will fail with error code `400 Bad Request`, and the error message will indicate the recommended endTime to use to retrieve a complete data set. This behavior may occur if the provided endTime=currentTime, since we are not a real time system. When `endTime` is not provided, the API returns the latest data.

For detailed information about the usage of the API, please refer to the Open API specification document - https://github.com/cisco-en-programmability/catalyst-center-api-specs/blob/main/Assurance/CE_Cat_Center_Org-fabricSiteHealthSummaries-1.0.1-resolved.yaml



    Args:
        startTime: Start time from which API queries the data set related to the resource. It must be specified in UNIX epochtime in milliseconds. Value is inclusive.

        endTime: End time to which API queries the data set related to the resource. It must be specified in UNIX epochtime in milliseconds. Value is inclusive.

        limit: Maximum number of records to return
        offset: Specifies the starting point within all records returned by the API. It's one based offset. The starting value is 1.
        sortBy: A field within the response to sort by.
        order: The sort order of the field ascending or descending.
        id: The list of entity Uuids. (Ex."6bef213c-19ca-4170-8375-b694e251101c")
Examples: id=6bef213c-19ca-4170-8375-b694e251101c (single entity uuid requested)
id=6bef213c-19ca-4170-8375-b694e251101c&id=32219612-819e-4b5e-a96b-cf22aca13dd9&id=2541e9a7-b80d-4955-8aa2-79b233318ba0 (multiple entity uuid with '&' separator)

        attribute: The list of FabricSite health attributes. Please refer to ```fabricSiteAttributes``` section in the Open API specification document mentioned in the description.
        view: The specific summary view being requested. A maximum of 3 views can be queried at a time per request.  Please refer to ```fabricSiteViews``` section in the Open API specification document mentioned in the description.
        siteHierarchy: The full hierarchical breakdown of the site tree starting from Global site name and ending with the specific site name. The Root site is named "Global" (Ex. `Global/AreaName/BuildingName/FloorName`)          This field supports wildcard asterisk (`*`) character search support. E.g. `*/San*, */San, /San*`          Examples:          `?siteHierarchy=Global/AreaName/BuildingName/FloorName` (single siteHierarchy requested)          `?siteHierarchy=Global/AreaName/BuildingName/FloorName&siteHierarchy=Global/AreaName2/BuildingName2/FloorName2` (multiple siteHierarchies requested)
        siteHierarchyId: The full hierarchy breakdown of the site tree in id form starting from Global site UUID and ending with the specific site UUID. (Ex. `globalUuid/areaUuid/buildingUuid/floorUuid`)          This field supports wildcard asterisk (`*`) character search support. E.g. `*uuid*, *uuid, uuid*`          Examples:          `?siteHierarchyId=globalUuid/areaUuid/buildingUuid/floorUuid `(single siteHierarchyId requested)          `?siteHierarchyId=globalUuid/areaUuid/buildingUuid/floorUuid&siteHierarchyId=globalUuid/areaUuid2/buildingUuid2/floorUuid2` (multiple siteHierarchyIds requested)
    """
    global client
    if not client:
        return {"error": "Not connected. Use connect() first."}

    kwargs = {}
    params = {}
    if startTime is not None:
        params['startTime'] = startTime
    if endTime is not None:
        params['endTime'] = endTime
    if limit is not None:
        params['limit'] = limit
    if offset is not None:
        params['offset'] = offset
    if sortBy is not None:
        params['sortBy'] = sortBy
    if order is not None:
        params['order'] = order
    if id is not None:
        params['id'] = id
    if attribute is not None:
        params['attribute'] = attribute
    if view is not None:
        params['view'] = view
    if siteHierarchy is not None:
        params['siteHierarchy'] = siteHierarchy
    if siteHierarchyId is not None:
        params['siteHierarchyId'] = siteHierarchyId
    if params:
        kwargs['params'] = params
    return await client.request('GET', f'/dna/data/api/v1/fabricSiteHealthSummaries', **kwargs)


@mcp.tool()
async def get_layer3_virtual_networks(virtualNetworkName: Optional[str] = None, fabricId: Optional[str] = None, anchoredSiteId: Optional[str] = None, offset: Optional[int] = None, limit: Optional[int] = None) -> Optional[Dict[str, Any]]:
    """Get layer 3 virtual networks

    Returns a list of layer 3 virtual networks that match the provided query parameters.


    Args:
        virtualNetworkName: Name of the layer 3 virtual network.
        fabricId: ID of the fabric the layer 3 virtual network is assigned to.
        anchoredSiteId: Fabric ID of the fabric site the layer 3 virtual network is anchored at.
        offset: Starting record for pagination.
        limit: Maximum number of records to return. The maximum number of objects supported in a single request is 500.
    """
    global client
    if not client:
        return {"error": "Not connected. Use connect() first."}

    kwargs = {}
    params = {}
    if virtualNetworkName is not None:
        params['virtualNetworkName'] = virtualNetworkName
    if fabricId is not None:
        params['fabricId'] = fabricId
    if anchoredSiteId is not None:
        params['anchoredSiteId'] = anchoredSiteId
    if offset is not None:
        params['offset'] = offset
    if limit is not None:
        params['limit'] = limit
    if params:
        kwargs['params'] = params
    return await client.request('GET', f'/dna/intent/api/v1/sda/layer3VirtualNetworks', **kwargs)

@mcp.tool()
async def delete_layer3_virtual_networks(virtualNetworkName: Optional[str] = None) -> Optional[Dict[str, Any]]:
    """Delete layer 3 virtual networks

    Deletes layer 3 virtual networks based on user input.

    Args:
        virtualNetworkName: Name of the layer 3 virtual network.
    """
    global client
    if not client:
        return {"error": "Not connected. Use connect() first."}

    kwargs = {}
    params = {}
    if virtualNetworkName is not None:
        params['virtualNetworkName'] = virtualNetworkName
    if params:
        kwargs['params'] = params
    return await client.request('DELETE', f'/dna/intent/api/v1/sda/layer3VirtualNetworks', **kwargs)

@mcp.tool()
async def add_layer3_virtual_networks(request_body: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Add layer 3 virtual networks

    Adds layer 3 virtual networks based on user input.

    Args:
        request_body: Request body data
    """
    global client
    if not client:
        return {"error": "Not connected. Use connect() first."}

    kwargs = {}
    kwargs['json'] = request_body
    return await client.request('POST', f'/dna/intent/api/v1/sda/layer3VirtualNetworks', **kwargs)


@mcp.tool()
async def read_virtual_network_with_its_health_summary_from_id(id: str, endTime: Optional[int] = None, startTime: Optional[int] = None, attribute: Optional[str] = None, view: Optional[str] = None) -> Optional[Dict[str, Any]]:
    """Read virtual network with its health summary from id

    Get health summary for a specific Virtual Network by providing the unique virtual networks id in the url path. L2 Virtual Networks are only included in health reporting for EVPN protocol deployments. The special Layer 3 VN called ‘INFRA_VN’ is also not included for user access through Assurance virtualNetworkHealthSummaries APIS. Please find INFRA_VN related health metrics under /data/api/v1/fabricSiteHealthSummaries (Ex: attributes ‘pubsubInfraVnGoodHealthPercentage’ and ‘bgpPeerInfraVnScoreGoodHealthPercentage’).

This API provides the latest health data until the given `endTime`. If data is not ready for the provided endTime, the request will fail with error code `400 Bad Request`, and the error message will indicate the recommended endTime to use to retrieve a complete data set. This behavior may occur if the provided endTime=currentTime, since we are not a real time system. When `endTime` is not provided, the API returns the latest data.

For detailed information about the usage of the API, please refer to the Open API specification document - https://github.com/cisco-en-programmability/catalyst-center-api-specs/blob/main/Assurance/CE_Cat_Center_Org-virtualNetworkHealthSummaries-1.0.1-resolved.yaml



    Args:
        id: unique virtual networks id
        endTime: End time to which API queries the data set related to the resource. It must be specified in UNIX epochtime in milliseconds. Value is inclusive.

        startTime: Start time from which API queries the data set related to the resource. It must be specified in UNIX epochtime in milliseconds. Value is inclusive.

        attribute: The interested fields in the request. For valid attributes, verify the documentation.
        view: The specific summary view being requested. This is an optional parameter which can be passed to get one or more of the specific health data summaries associated with virtual networks.
    """
    global client
    if not client:
        return {"error": "Not connected. Use connect() first."}

    kwargs = {}
    params = {}
    if endTime is not None:
        params['endTime'] = endTime
    if startTime is not None:
        params['startTime'] = startTime
    if attribute is not None:
        params['attribute'] = attribute
    if view is not None:
        params['view'] = view
    if params:
        kwargs['params'] = params
    return await client.request('GET', f'/dna/data/api/v1/virtualNetworkHealthSummaries/{id}', **kwargs)


@mcp.tool()
async def get_port_assignment_count(fabricId: Optional[str] = None, networkDeviceId: Optional[str] = None, interfaceName: Optional[str] = None, dataVlanName: Optional[str] = None, voiceVlanName: Optional[str] = None) -> Optional[Dict[str, Any]]:
    """Get port assignment count

    Returns the count of port assignments that match the provided query parameters.

    Args:
        fabricId: ID of the fabric the device is assigned to.
        networkDeviceId: Network device ID of the port assignment.
        interfaceName: Interface name of the port assignment.
        dataVlanName: Data VLAN name of the port assignment.
        voiceVlanName: Voice VLAN name of the port assignment.
    """
    global client
    if not client:
        return {"error": "Not connected. Use connect() first."}

    kwargs = {}
    params = {}
    if fabricId is not None:
        params['fabricId'] = fabricId
    if networkDeviceId is not None:
        params['networkDeviceId'] = networkDeviceId
    if interfaceName is not None:
        params['interfaceName'] = interfaceName
    if dataVlanName is not None:
        params['dataVlanName'] = dataVlanName
    if voiceVlanName is not None:
        params['voiceVlanName'] = voiceVlanName
    if params:
        kwargs['params'] = params
    return await client.request('GET', f'/dna/intent/api/v1/sda/portAssignments/count', **kwargs)

@mcp.tool()
async def get_pending_fabric_events(fabricId: Optional[str] = None, offset: Optional[int] = None, limit: Optional[int] = None) -> Optional[Dict[str, Any]]:
    """Get pending fabric events

    Returns a list of pending fabric events that match the provided query parameters.

    Args:
        fabricId: ID of the fabric.
        offset: Starting record for pagination.
        limit: Maximum number of records to return. The maximum number of objects supported in a single request is 500.
    """
    global client
    if not client:
        return {"error": "Not connected. Use connect() first."}

    kwargs = {}
    params = {}
    if fabricId is not None:
        params['fabricId'] = fabricId
    if offset is not None:
        params['offset'] = offset
    if limit is not None:
        params['limit'] = limit
    if params:
        kwargs['params'] = params
    return await client.request('GET', f'/dna/intent/api/v1/sda/pendingFabricEvents', **kwargs)

@mcp.tool()
async def reprovision_devices(request_body: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Re-provision devices

    Re-provisions network devices to the site based on the user input.

    Args:
        request_body: Request body data
    """
    global client
    if not client:
        return {"error": "Not connected. Use connect() first."}

    kwargs = {}
    kwargs['json'] = request_body
    return await client.request('PUT', f'/dna/intent/api/v1/sda/provisionDevices', **kwargs)

@mcp.tool()
async def provision_devices(request_body: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Provision devices

    Provisions network devices to respective Sites based on user input.

    Args:
        request_body: Request body data
    """
    global client
    if not client:
        return {"error": "Not connected. Use connect() first."}

    kwargs = {}
    kwargs['json'] = request_body
    return await client.request('POST', f'/dna/intent/api/v1/sda/provisionDevices', **kwargs)

@mcp.tool()
async def get_provisioned_devices(id: Optional[str] = None, networkDeviceId: Optional[str] = None, siteId: Optional[str] = None, offset: Optional[int] = None, limit: Optional[int] = None) -> Optional[Dict[str, Any]]:
    """Get provisioned devices

    Returns the list of provisioned devices based on query parameters.

    Args:
        id: ID of the provisioned device.
        networkDeviceId: ID of the network device.
        siteId: ID of the site hierarchy.
        offset: Starting record for pagination.
        limit: Maximum number of devices to return. The maximum number of objects supported in a single request is 500.
    """
    global client
    if not client:
        return {"error": "Not connected. Use connect() first."}

    kwargs = {}
    params = {}
    if id is not None:
        params['id'] = id
    if networkDeviceId is not None:
        params['networkDeviceId'] = networkDeviceId
    if siteId is not None:
        params['siteId'] = siteId
    if offset is not None:
        params['offset'] = offset
    if limit is not None:
        params['limit'] = limit
    if params:
        kwargs['params'] = params
    return await client.request('GET', f'/dna/intent/api/v1/sda/provisionDevices', **kwargs)



@mcp.tool()
async def get_layer2_virtual_network_count(fabricId: Optional[str] = None, vlanName: Optional[str] = None, vlanId: Optional[int] = None, trafficType: Optional[str] = None, associatedLayer3VirtualNetworkName: Optional[str] = None) -> Optional[Dict[str, Any]]:
    """Get layer 2 virtual network count

    Returns the count of layer 2 virtual networks that match the provided query parameters.

    Args:
        fabricId: ID of the fabric the layer 2 virtual network is assigned to.
        vlanName: The vlan name of the layer 2 virtual network.
        vlanId: The vlan ID of the layer 2 virtual network.
        trafficType: The traffic type of the layer 2 virtual network.
        associatedLayer3VirtualNetworkName: Name of the associated layer 3 virtual network.
    """
    global client
    if not client:
        return {"error": "Not connected. Use connect() first."}

    kwargs = {}
    params = {}
    if fabricId is not None:
        params['fabricId'] = fabricId
    if vlanName is not None:
        params['vlanName'] = vlanName
    if vlanId is not None:
        params['vlanId'] = vlanId
    if trafficType is not None:
        params['trafficType'] = trafficType
    if associatedLayer3VirtualNetworkName is not None:
        params['associatedLayer3VirtualNetworkName'] = associatedLayer3VirtualNetworkName
    if params:
        kwargs['params'] = params
    return await client.request('GET', f'/dna/intent/api/v1/sda/layer2VirtualNetworks/count', **kwargs)

@mcp.tool()
async def update_fabric_devices(request_body: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Update fabric devices

    Updates fabric devices based on user input.

    Args:
        request_body: Request body data
    """
    global client
    if not client:
        return {"error": "Not connected. Use connect() first."}

    kwargs = {}
    kwargs['json'] = request_body
    return await client.request('PUT', f'/dna/intent/api/v1/sda/fabricDevices', **kwargs)

@mcp.tool()
async def get_fabric_devices(fabricId: str, networkDeviceId: Optional[str] = None, deviceRoles: Optional[str] = None, offset: Optional[int] = None, limit: Optional[int] = None) -> Optional[Dict[str, Any]]:
    """Get fabric devices

    Returns a list of fabric devices that match the provided query parameters.


    Args:
        fabricId: ID of the fabric this device belongs to.
        networkDeviceId: Network device ID of the fabric device.
        deviceRoles: Device roles of the fabric device. Allowed values are [CONTROL_PLANE_NODE, EDGE_NODE, BORDER_NODE, WIRELESS_CONTROLLER_NODE, EXTENDED_NODE].
        offset: Starting record for pagination.
        limit: Maximum number of records to return. The maximum number of objects supported in a single request is 500.
    """
    global client
    if not client:
        return {"error": "Not connected. Use connect() first."}

    kwargs = {}
    params = {}
    if fabricId is not None:
        params['fabricId'] = fabricId
    if networkDeviceId is not None:
        params['networkDeviceId'] = networkDeviceId
    if deviceRoles is not None:
        params['deviceRoles'] = deviceRoles
    if offset is not None:
        params['offset'] = offset
    if limit is not None:
        params['limit'] = limit
    if params:
        kwargs['params'] = params
    return await client.request('GET', f'/dna/intent/api/v1/sda/fabricDevices', **kwargs)


@mcp.tool()
async def add_fabric_zone(request_body: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Add fabric zone

    Adds a fabric zone based on user input.

    Args:
        request_body: Request body data
    """
    global client
    if not client:
        return {"error": "Not connected. Use connect() first."}

    kwargs = {}
    kwargs['json'] = request_body
    return await client.request('POST', f'/dna/intent/api/v1/sda/fabricZones', **kwargs)

@mcp.tool()
async def get_fabric_zones(id: Optional[str] = None, siteId: Optional[str] = None, offset: Optional[int] = None, limit: Optional[int] = None) -> Optional[Dict[str, Any]]:
    """Get fabric zones

    Returns a list of fabric zones that match the provided query parameters.

    Args:
        id: ID of the fabric zone.
        siteId: ID of the network hierarchy associated with the fabric zone.
        offset: Starting record for pagination.
        limit: Maximum number of records to return. The maximum number of objects supported in a single request is 500.
    """
    global client
    if not client:
        return {"error": "Not connected. Use connect() first."}

    kwargs = {}
    params = {}
    if id is not None:
        params['id'] = id
    if siteId is not None:
        params['siteId'] = siteId
    if offset is not None:
        params['offset'] = offset
    if limit is not None:
        params['limit'] = limit
    if params:
        kwargs['params'] = params
    return await client.request('GET', f'/dna/intent/api/v1/sda/fabricZones', **kwargs)

@mcp.tool()
async def update_fabric_zone(request_body: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Update fabric zone

    Updates a fabric zone based on user input.

    Args:
        request_body: Request body data
    """
    global client
    if not client:
        return {"error": "Not connected. Use connect() first."}

    kwargs = {}
    kwargs['json'] = request_body
    return await client.request('PUT', f'/dna/intent/api/v1/sda/fabricZones', **kwargs)

@mcp.tool()
async def get_fabric_site_trend_analytics(id: str, trendInterval: str, startTime: Optional[int] = None, endTime: Optional[int] = None, limit: Optional[int] = None, offset: Optional[int] = None, order: Optional[str] = None, attribute: Optional[str] = None) -> Optional[Dict[str, Any]]:
    """The Trend analytics data for a fabric site in the specified time range

    Get health time series for a specific Fabric Site by providing the unique Fabric site id in the url path.
The data will be grouped based on the specified trend time interval. If startTime and endTime are not provided, the API defaults to the last 24 hours.

By default:
- the number of records returned will be 500.
- the records will be sorted in time ascending (`asc`) order

ex: id:93a25378-7740-4e20-8d90-0060ad9a1be0

This API provides the latest health data until the given `endTime`. If data is not ready for the provided endTime, the request will fail with error code `400 Bad Request`, and the error message will indicate the recommended endTime to use to retrieve a complete data set. This behavior may occur if the provided endTime=currentTime, since we are not a real time system. When `endTime` is not provided, the API returns the latest data.

For detailed information about the usage of the API, please refer to the Open API specification document - https://github.com/cisco-en-programmability/catalyst-center-api-specs/blob/main/Assurance/CE_Cat_Center_Org-fabricSiteHealthSummaries-1.0.1-resolved.yaml

    Args:
        id: unique fabric site id
        startTime: Start time from which API queries the data set related to the resource. It must be specified in UNIX epochtime in milliseconds. Value is inclusive.

        endTime: End time to which API queries the data set related to the resource. It must be specified in UNIX epochtime in milliseconds. Value is inclusive.

        trendInterval: The time window to aggregate the metrics.
Interval can be 5 minutes or 10 minutes or 1 hour or 1 day or 7 days

        limit: Maximum number of records to return
        offset: Specifies the starting point within all records returned by the API. It's one based offset. The starting value is 1.
        order: The sort order of the field ascending or descending.
        attribute:  The interested fields in the request. For valid attributes, verify the documentation.
    """
    global client
    if not client:
        return {"error": "Not connected. Use connect() first."}

    kwargs = {}
    params = {}
    if startTime is not None:
        params['startTime'] = startTime
    if endTime is not None:
        params['endTime'] = endTime
    if trendInterval is not None:
        params['trendInterval'] = trendInterval
    if limit is not None:
        params['limit'] = limit
    if offset is not None:
        params['offset'] = offset
    if order is not None:
        params['order'] = order
    if attribute is not None:
        params['attribute'] = attribute
    if params:
        kwargs['params'] = params
    return await client.request('GET', f'/dna/data/api/v1/fabricSiteHealthSummaries/{id}/trendAnalytics', **kwargs)


@mcp.tool()
async def readiness_status_for_a_fabric_site(id: str, order: Optional[str] = None) -> Optional[Dict[str, Any]]:
    """Readiness status for a fabric site.

    Gets a list of SDA virtual networks for the specified fabric site, including their individual readiness status for Security Service Insertion (SSI) deployment. The result is sorted by virtualNetworkName.

    Args:
        id: Sda fabric site id.
        order: Whether ascending or descending order should be used to sort the response.
    """
    global client
    if not client:
        return {"error": "Not connected. Use connect() first."}

    kwargs = {}
    params = {}
    if order is not None:
        params['order'] = order
    if params:
        kwargs['params'] = params
    return await client.request('GET', f'/dna/intent/api/v1/securityServiceInsertion/fabricSitesReadiness/{id}', **kwargs)


@mcp.tool()
async def add_fabric_site(request_body: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Add fabric site

    Adds a fabric site based on user input.

    Args:
        request_body: Request body data
    """
    global client
    if not client:
        return {"error": "Not connected. Use connect() first."}

    kwargs = {}
    kwargs['json'] = request_body
    return await client.request('POST', f'/dna/intent/api/v1/sda/fabricSites', **kwargs)

@mcp.tool()
async def update_fabric_site(request_body: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Update fabric site

    Updates a fabric site based on user input.

    Args:
        request_body: Request body data
    """
    global client
    if not client:
        return {"error": "Not connected. Use connect() first."}

    kwargs = {}
    kwargs['json'] = request_body
    return await client.request('PUT', f'/dna/intent/api/v1/sda/fabricSites', **kwargs)

@mcp.tool()
async def get_fabric_sites(id: Optional[str] = None, siteId: Optional[str] = None, offset: Optional[int] = None, limit: Optional[int] = None) -> Optional[Dict[str, Any]]:
    """Get fabric sites

    Returns a list of fabric sites that match the provided query parameters.

    Args:
        id: ID of the fabric site.
        siteId: ID of the network hierarchy associated with the fabric site.
        offset: Starting record for pagination.
        limit: Maximum number of records to return. The maximum number of objects supported in a single request is 500.
    """
    global client
    if not client:
        return {"error": "Not connected. Use connect() first."}

    kwargs = {}
    params = {}
    if id is not None:
        params['id'] = id
    if siteId is not None:
        params['siteId'] = siteId
    if offset is not None:
        params['offset'] = offset
    if limit is not None:
        params['limit'] = limit
    if params:
        kwargs['params'] = params
    return await client.request('GET', f'/dna/intent/api/v1/sda/fabricSites', **kwargs)

@mcp.tool()
async def get_layer3_virtual_networks_count(fabricId: Optional[str] = None, anchoredSiteId: Optional[str] = None) -> Optional[Dict[str, Any]]:
    """Get layer 3 virtual networks count

    Returns the count of layer 3 virtual networks that match the provided query parameters.

    Args:
        fabricId: ID of the fabric the layer 3 virtual network is assigned to.
        anchoredSiteId: Fabric ID of the fabric site the layer 3 virtual network is anchored at.
    """
    global client
    if not client:
        return {"error": "Not connected. Use connect() first."}

    kwargs = {}
    params = {}
    if fabricId is not None:
        params['fabricId'] = fabricId
    if anchoredSiteId is not None:
        params['anchoredSiteId'] = anchoredSiteId
    if params:
        kwargs['params'] = params
    return await client.request('GET', f'/dna/intent/api/v1/sda/layer3VirtualNetworks/count', **kwargs)

@mcp.tool()
async def get_fabric_devices_count(fabricId: str, networkDeviceId: Optional[str] = None, deviceRoles: Optional[str] = None) -> Optional[Dict[str, Any]]:
    """Get fabric devices count

    Returns the count of fabric devices that match the provided query parameters.

    Args:
        fabricId: ID of the fabric this device belongs to.
        networkDeviceId: Network device ID of the fabric device.
        deviceRoles: Device roles of the fabric device. Allowed values are [CONTROL_PLANE_NODE, EDGE_NODE, BORDER_NODE, WIRELESS_CONTROLLER_NODE, EXTENDED_NODE].
    """
    global client
    if not client:
        return {"error": "Not connected. Use connect() first."}

    kwargs = {}
    params = {}
    if fabricId is not None:
        params['fabricId'] = fabricId
    if networkDeviceId is not None:
        params['networkDeviceId'] = networkDeviceId
    if deviceRoles is not None:
        params['deviceRoles'] = deviceRoles
    if params:
        kwargs['params'] = params
    return await client.request('GET', f'/dna/intent/api/v1/sda/fabricDevices/count', **kwargs)

@mcp.tool()
async def read_list_of_virtual_networks_with_their_health_summary(startTime: Optional[int] = None, endTime: Optional[int] = None, limit: Optional[int] = None, offset: Optional[int] = None, sortBy: Optional[str] = None, order: Optional[str] = None, id: Optional[str] = None, vnLayer: Optional[str] = None, attribute: Optional[str] = None, view: Optional[str] = None, siteHierarchy: Optional[str] = None, SiteHierarchyId: Optional[str] = None) -> Optional[Dict[str, Any]]:
    """Read list of Virtual Networks with their health summary

    Get a paginated list of Virtual Networks with health summary. Layer 2 Virtual Networks are only included in health reporting for EVPN protocol deployments. The special Layer 3 VN called ‘INFRA_VN’ is also not included for user access through Assurance virtualNetworkHealthSummaries APIS. Please find INFRA_VN related health metrics under /data/api/v1/fabricSiteHealthSummaries (Ex: attributes ‘pubsubInfraVnGoodHealthPercentage’ and ‘bgpPeerInfraVnScoreGoodHealthPercentage’).

This API provides the latest health data until the given `endTime`. If data is not ready for the provided endTime, the request will fail with error code `400 Bad Request`, and the error message will indicate the recommended endTime to use to retrieve a complete data set. This behavior may occur if the provided endTime=currentTime, since we are not a real time system. When `endTime` is not provided, the API returns the latest data.

For detailed information about the usage of the API, please refer to the Open API specification document - https://github.com/cisco-en-programmability/catalyst-center-api-specs/blob/main/Assurance/CE_Cat_Center_Org-virtualNetworkHealthSummaries-1.0.1-resolved.yaml


    Args:
        startTime: Start time from which API queries the data set related to the resource. It must be specified in UNIX epochtime in milliseconds. Value is inclusive.

        endTime: End time to which API queries the data set related to the resource. It must be specified in UNIX epochtime in milliseconds. Value is inclusive.

        limit: Maximum number of records to return
        offset: Specifies the starting point within all records returned by the API. It's one based offset. The starting value is 1.
        sortBy: A field within the response to sort by.
        order: The sort order of the field ascending or descending.
        id: The list of entity Uuids. (Ex."6bef213c-19ca-4170-8375-b694e251101c")
Examples: id=6bef213c-19ca-4170-8375-b694e251101c (single entity uuid requested)
id=6bef213c-19ca-4170-8375-b694e251101c&id=32219612-819e-4b5e-a96b-cf22aca13dd9&id=2541e9a7-b80d-4955-8aa2-79b233318ba0 (multiple entity uuid with '&' separator)

        vnLayer: VN Layer information covering Layer 3 or Layer 2 VNs.

        attribute: The interested fields in the request. For valid attributes, verify the documentation.
        view: The specific summary view being requested. This is an optional parameter which can be passed to get one or more of the specific health data summaries associated with virtual networks.
        siteHierarchy: The full hierarchical breakdown of the site tree starting from Global site name and ending with the specific site name. The Root site is named "Global" (Ex. `Global/AreaName/BuildingName/FloorName`)          This field supports wildcard asterisk (`*`) character search support. E.g. `*/San*, */San, /San*`          Examples:          `?siteHierarchy=Global/AreaName/BuildingName/FloorName` (single siteHierarchy requested)          `?siteHierarchy=Global/AreaName/BuildingName/FloorName&siteHierarchy=Global/AreaName2/BuildingName2/FloorName2` (multiple siteHierarchies requested)
        SiteHierarchyId: The full hierarchy breakdown of the site tree in id form starting from Global site UUID and ending with the specific site UUID. (Ex. `globalUuid/areaUuid/buildingUuid/floorUuid`)          This field supports wildcard asterisk (`*`) character search support. E.g. `*uuid*, *uuid, uuid*`          Examples:          `?siteHierarchyId=globalUuid/areaUuid/buildingUuid/floorUuid `(single siteHierarchyId requested)          `?siteHierarchyId=globalUuid/areaUuid/buildingUuid/floorUuid&siteHierarchyId=globalUuid/areaUuid2/buildingUuid2/floorUuid2` (multiple siteHierarchyIds requested)
    """
    global client
    if not client:
        return {"error": "Not connected. Use connect() first."}

    kwargs = {}
    params = {}
    if startTime is not None:
        params['startTime'] = startTime
    if endTime is not None:
        params['endTime'] = endTime
    if limit is not None:
        params['limit'] = limit
    if offset is not None:
        params['offset'] = offset
    if sortBy is not None:
        params['sortBy'] = sortBy
    if order is not None:
        params['order'] = order
    if id is not None:
        params['id'] = id
    if vnLayer is not None:
        params['vnLayer'] = vnLayer
    if attribute is not None:
        params['attribute'] = attribute
    if view is not None:
        params['view'] = view
    if siteHierarchy is not None:
        params['siteHierarchy'] = siteHierarchy
    if SiteHierarchyId is not None:
        params['SiteHierarchyId'] = SiteHierarchyId
    if params:
        kwargs['params'] = params
    return await client.request('GET', f'/dna/data/api/v1/virtualNetworkHealthSummaries', **kwargs)


@mcp.tool()
async def get_multicast(fabricId: Optional[str] = None, offset: Optional[int] = None, limit: Optional[int] = None) -> Optional[Dict[str, Any]]:
    """Get multicast

    Returns a list of multicast configurations at a fabric site level that match the provided query parameters.

    Args:
        fabricId: ID of the fabric site where multicast is configured.
        offset: Starting record for pagination.
        limit: Maximum number of records to return. The maximum number of objects supported in a single request is 500.
    """
    global client
    if not client:
        return {"error": "Not connected. Use connect() first."}

    kwargs = {}
    params = {}
    if fabricId is not None:
        params['fabricId'] = fabricId
    if offset is not None:
        params['offset'] = offset
    if limit is not None:
        params['limit'] = limit
    if params:
        kwargs['params'] = params
    return await client.request('GET', f'/dna/intent/api/v1/sda/multicast', **kwargs)

@mcp.tool()
async def read_virtual_networks_count(startTime: Optional[int] = None, endTime: Optional[int] = None, id: Optional[str] = None, vnLayer: Optional[str] = None, siteHierarchy: Optional[str] = None, siteHierarchyId: Optional[str] = None) -> Optional[Dict[str, Any]]:
    """Read Virtual Networks count

    Get a count of virtual networks. Use available query parameters to get the count of a subset of virtual networks. Layer 2 Virtual Networks are only included for EVPN protocol deployments. The special Layer 3 VN called ‘INFRA_VN’ is also not included.

This API provides the latest health data until the given `endTime`. If data is not ready for the provided endTime, the request will fail with error code `400 Bad Request`, and the error message will indicate the recommended endTime to use to retrieve a complete data set. This behavior may occur if the provided endTime=currentTime, since we are not a real time system. When `endTime` is not provided, the API returns the latest data.

For detailed information about the usage of the API, please refer to the Open API specification document - https://github.com/cisco-en-programmability/catalyst-center-api-specs/blob/main/Assurance/CE_Cat_Center_Org-virtualNetworkHealthSummaries-1.0.1-resolved.yaml


    Args:
        startTime: Start time from which API queries the data set related to the resource. It must be specified in UNIX epochtime in milliseconds. Value is inclusive.

        endTime: End time to which API queries the data set related to the resource. It must be specified in UNIX epochtime in milliseconds. Value is inclusive.

        id: The list of entity Uuids. (Ex."6bef213c-19ca-4170-8375-b694e251101c")
Examples: id=6bef213c-19ca-4170-8375-b694e251101c (single entity uuid requested)
id=6bef213c-19ca-4170-8375-b694e251101c&id=32219612-819e-4b5e-a96b-cf22aca13dd9&id=2541e9a7-b80d-4955-8aa2-79b233318ba0 (multiple entity uuid with '&' separator)

        vnLayer: VN Layer information covering Layer 3 or Layer 2 VNs.

        siteHierarchy: The full hierarchical breakdown of the site tree starting from Global site name and ending with the specific site name. The Root site is named "Global" (Ex. `Global/AreaName/BuildingName/FloorName`)          This field supports wildcard asterisk (`*`) character search support. E.g. `*/San*, */San, /San*`          Examples:          `?siteHierarchy=Global/AreaName/BuildingName/FloorName` (single siteHierarchy requested)          `?siteHierarchy=Global/AreaName/BuildingName/FloorName&siteHierarchy=Global/AreaName2/BuildingName2/FloorName2` (multiple siteHierarchies requested)
        siteHierarchyId: The full hierarchy breakdown of the site tree in id form starting from Global site UUID and ending with the specific site UUID. (Ex. `globalUuid/areaUuid/buildingUuid/floorUuid`)          This field supports wildcard asterisk (`*`) character search support. E.g. `*uuid*, *uuid, uuid*`          Examples:          `?siteHierarchyId=globalUuid/areaUuid/buildingUuid/floorUuid `(single siteHierarchyId requested)          `?siteHierarchyId=globalUuid/areaUuid/buildingUuid/floorUuid&siteHierarchyId=globalUuid/areaUuid2/buildingUuid2/floorUuid2` (multiple siteHierarchyIds requested)
    """
    global client
    if not client:
        return {"error": "Not connected. Use connect() first."}

    kwargs = {}
    params = {}
    if startTime is not None:
        params['startTime'] = startTime
    if endTime is not None:
        params['endTime'] = endTime
    if id is not None:
        params['id'] = id
    if vnLayer is not None:
        params['vnLayer'] = vnLayer
    if siteHierarchy is not None:
        params['siteHierarchy'] = siteHierarchy
    if siteHierarchyId is not None:
        params['siteHierarchyId'] = siteHierarchyId
    if params:
        kwargs['params'] = params
    return await client.request('GET', f'/dna/data/api/v1/virtualNetworkHealthSummaries/count', **kwargs)

@mcp.tool()
async def get_virtual_network_trend_analytics(id: str, trendInterval: str, startTime: Optional[int] = None, endTime: Optional[int] = None, limit: Optional[int] = None, offset: Optional[int] = None, order: Optional[str] = None, attribute: Optional[str] = None) -> Optional[Dict[str, Any]]:
    """The Trend analytics data for a virtual network in the specified time range


Get health time series for a specific Virtual Network by providing the unique Virtual Network id in the url path. Layer 2 Virtual Networks are only included in health reporting for EVPN protocol deployments. The special Layer 3 VN called ‘INFRA_VN’ is also not included for user access through Assurance virtualNetworkHealthSummaries APIS.

The data will be grouped based on the specified trend time interval. If startTime and endTime are not provided, the API defaults to the last 24 hours.

By default:
- the number of records returned will be 500.
- the records will be sorted in time ascending (`asc`) order

For EVPN , {id} is a combination of VN:FabrisiteId. ex: L2VN1:93a25378-7740-4e20-8d90-0060ad9a1be0

This API provides the latest health data until the given `endTime`. If data is not ready for the provided endTime, the request will fail with error code `400 Bad Request`, and the error message will indicate the recommended endTime to use to retrieve a complete data set. This behavior may occur if the provided endTime=currentTime, since we are not a real time system. When `endTime` is not provided, the API returns the latest data.

For detailed information about the usage of the API, please refer to the Open API specification document - https://github.com/cisco-en-programmability/catalyst-center-api-specs/blob/main/Assurance/CE_Cat_Center_Org-virtualNetworkHealthSummaries-1.0.1-resolved.yaml


    Args:
        id: unique virtual network id
        startTime: Start time from which API queries the data set related to the resource. It must be specified in UNIX epochtime in milliseconds. Value is inclusive.

        endTime: End time to which API queries the data set related to the resource. It must be specified in UNIX epochtime in milliseconds. Value is inclusive.

        trendInterval: The time window to aggregate the metrics.
Interval can be 5 minutes or 10 minutes or 1 hour or 1 day or 7 days

        limit: Maximum number of records to return
        offset: Specifies the starting point within all records returned by the API. It's one based offset. The starting value is 1.
        order: The sort order of the field ascending or descending.
        attribute: The interested fields in the request. For valid attributes, verify the documentation.
    """
    global client
    if not client:
        return {"error": "Not connected. Use connect() first."}

    kwargs = {}
    params = {}
    if startTime is not None:
        params['startTime'] = startTime
    if endTime is not None:
        params['endTime'] = endTime
    if trendInterval is not None:
        params['trendInterval'] = trendInterval
    if limit is not None:
        params['limit'] = limit
    if offset is not None:
        params['offset'] = offset
    if order is not None:
        params['order'] = order
    if attribute is not None:
        params['attribute'] = attribute
    if params:
        kwargs['params'] = params
    return await client.request('GET', f'/dna/data/api/v1/virtualNetworkHealthSummaries/{id}/trendAnalytics', **kwargs)

@mcp.tool()
async def get_port_assignments(fabricId: Optional[str] = None, networkDeviceId: Optional[str] = None, interfaceName: Optional[str] = None, dataVlanName: Optional[str] = None, voiceVlanName: Optional[str] = None, offset: Optional[int] = None, limit: Optional[int] = None) -> Optional[Dict[str, Any]]:
    """Get port assignments

    Returns a list of port assignments that match the provided query parameters.

    Args:
        fabricId: ID of the fabric the device is assigned to.
        networkDeviceId: Network device ID of the port assignment.
        interfaceName: Interface name of the port assignment.
        dataVlanName: Data VLAN name of the port assignment.
        voiceVlanName: Voice VLAN name of the port assignment.
        offset: Starting record for pagination.
        limit: Maximum number of records to return. The maximum number of objects supported in a single request is 500.
    """
    global client
    if not client:
        return {"error": "Not connected. Use connect() first."}

    kwargs = {}
    params = {}
    if fabricId is not None:
        params['fabricId'] = fabricId
    if networkDeviceId is not None:
        params['networkDeviceId'] = networkDeviceId
    if interfaceName is not None:
        params['interfaceName'] = interfaceName
    if dataVlanName is not None:
        params['dataVlanName'] = dataVlanName
    if voiceVlanName is not None:
        params['voiceVlanName'] = voiceVlanName
    if offset is not None:
        params['offset'] = offset
    if limit is not None:
        params['limit'] = limit
    if params:
        kwargs['params'] = params
    return await client.request('GET', f'/dna/intent/api/v1/sda/portAssignments', **kwargs)

@mcp.tool()
async def add_port_assignments(request_body: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Add port assignments

    Adds port assignments based on user input.

    Args:
        request_body: Request body data
    """
    global client
    if not client:
        return {"error": "Not connected. Use connect() first."}

    kwargs = {}
    kwargs['json'] = request_body
    return await client.request('POST', f'/dna/intent/api/v1/sda/portAssignments', **kwargs)

@mcp.tool()
async def update_port_assignments(request_body: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Update port assignments

    Updates port assignments based on user input.

    Args:
        request_body: Request body data
    """
    global client
    if not client:
        return {"error": "Not connected. Use connect() first."}

    kwargs = {}
    kwargs['json'] = request_body
    return await client.request('PUT', f'/dna/intent/api/v1/sda/portAssignments', **kwargs)

@mcp.tool()
async def read_fabric_site_count(startTime: Optional[int] = None, endTime: Optional[int] = None, id: Optional[str] = None, siteHierarchy: Optional[str] = None, siteHierarchyId: Optional[str] = None) -> Optional[Dict[str, Any]]:
    """Read fabric site count

    Get a count of Fabric sites. Use available query parameters to get the count of a subset of fabric sites.

This API provides the latest health data until the given `endTime`. If data is not ready for the provided endTime, the request will fail with error code `400 Bad Request`, and the error message will indicate the recommended endTime to use to retrieve a complete data set. This behavior may occur if the provided endTime=currentTime, since we are not a real time system. When `endTime` is not provided, the API returns the latest data.

For detailed information about the usage of the API, please refer to the Open API specification document - https://github.com/cisco-en-programmability/catalyst-center-api-specs/blob/main/Assurance/CE_Cat_Center_Org-fabricSiteHealthSummaries-1.0.1-resolved.yaml

    Args:
        startTime: Start time from which API queries the data set related to the resource. It must be specified in UNIX epochtime in milliseconds. Value is inclusive.

        endTime: End time to which API queries the data set related to the resource. It must be specified in UNIX epochtime in milliseconds. Value is inclusive.

        id: The list of entity Uuids. (Ex."6bef213c-19ca-4170-8375-b694e251101c")
Examples: id=6bef213c-19ca-4170-8375-b694e251101c (single entity uuid requested)
id=6bef213c-19ca-4170-8375-b694e251101c&id=32219612-819e-4b5e-a96b-cf22aca13dd9&id=2541e9a7-b80d-4955-8aa2-79b233318ba0 (multiple entity uuid with '&' separator)

        siteHierarchy: The full hierarchical breakdown of the site tree starting from Global site name and ending with the specific site name. The Root site is named "Global" (Ex. `Global/AreaName/BuildingName/FloorName`)          This field supports wildcard asterisk (`*`) character search support. E.g. `*/San*, */San, /San*`          Examples:          `?siteHierarchy=Global/AreaName/BuildingName/FloorName` (single siteHierarchy requested)          `?siteHierarchy=Global/AreaName/BuildingName/FloorName&siteHierarchy=Global/AreaName2/BuildingName2/FloorName2` (multiple siteHierarchies requested)
        siteHierarchyId: The full hierarchy breakdown of the site tree in id form starting from Global site UUID and ending with the specific site UUID. (Ex. `globalUuid/areaUuid/buildingUuid/floorUuid`)          This field supports wildcard asterisk (`*`) character search support. E.g. `*uuid*, *uuid, uuid*`          Examples:          `?siteHierarchyId=globalUuid/areaUuid/buildingUuid/floorUuid `(single siteHierarchyId requested)          `?siteHierarchyId=globalUuid/areaUuid/buildingUuid/floorUuid&siteHierarchyId=globalUuid/areaUuid2/buildingUuid2/floorUuid2` (multiple siteHierarchyIds requested)
    """
    global client
    if not client:
        return {"error": "Not connected. Use connect() first."}

    kwargs = {}
    params = {}
    if startTime is not None:
        params['startTime'] = startTime
    if endTime is not None:
        params['endTime'] = endTime
    if id is not None:
        params['id'] = id
    if siteHierarchy is not None:
        params['siteHierarchy'] = siteHierarchy
    if siteHierarchyId is not None:
        params['siteHierarchyId'] = siteHierarchyId
    if params:
        kwargs['params'] = params
    return await client.request('GET', f'/dna/data/api/v1/fabricSiteHealthSummaries/count', **kwargs)

@mcp.tool()
async def get_anycast_gateway_count(fabricId: Optional[str] = None, virtualNetworkName: Optional[str] = None, ipPoolName: Optional[str] = None, vlanName: Optional[str] = None, vlanId: Optional[int] = None) -> Optional[Dict[str, Any]]:
    """Get anycast gateway count

    Returns the count of anycast gateways that match the provided query parameters.

    Args:
        fabricId: ID of the fabric the anycast gateway is assigned to.
        virtualNetworkName: Name of the virtual network associated with the anycast gateways.
        ipPoolName: Name of the IP pool associated with the anycast gateways.
        vlanName: VLAN name of the anycast gateways.
        vlanId: VLAN ID of the anycast gateways. The allowed range for vlanId is [2-4093] except for reserved VLANs [1002-1005], 2046, and 4094.
    """
    global client
    if not client:
        return {"error": "Not connected. Use connect() first."}

    kwargs = {}
    params = {}
    if fabricId is not None:
        params['fabricId'] = fabricId
    if virtualNetworkName is not None:
        params['virtualNetworkName'] = virtualNetworkName
    if ipPoolName is not None:
        params['ipPoolName'] = ipPoolName
    if vlanName is not None:
        params['vlanName'] = vlanName
    if vlanId is not None:
        params['vlanId'] = vlanId
    if params:
        kwargs['params'] = params
    return await client.request('GET', f'/dna/intent/api/v1/sda/anycastGateways/count', **kwargs)

@mcp.tool()
async def get_provisioned_devices_count(siteId: Optional[str] = None) -> Optional[Dict[str, Any]]:
    """Get Provisioned Devices count

    Returns the count of provisioned devices based on query parameters.


    Args:
        siteId: ID of the site hierarchy.
    """
    global client
    if not client:
        return {"error": "Not connected. Use connect() first."}

    kwargs = {}
    params = {}
    if siteId is not None:
        params['siteId'] = siteId
    if params:
        kwargs['params'] = params
    return await client.request('GET', f'/dna/intent/api/v1/sda/provisionDevices/count', **kwargs)


@mcp.tool()
async def get_edge_device_from_sda_fabric(deviceManagementIpAddress: str) -> Optional[Dict[str, Any]]:
    """Get edge device from SDA Fabric

    Args:
        deviceManagementIpAddress: deviceManagementIpAddress
    """
    global client
    if not client:
        return {"error": "Not connected. Use connect() first."}

    kwargs = {}
    params = {}
    if deviceManagementIpAddress is not None:
        params['deviceManagementIpAddress'] = deviceManagementIpAddress
    if params:
        kwargs['params'] = params
    return await client.request('GET', f'/dna/intent/api/v1/business/sda/edge-device', **kwargs)

@mcp.tool()
async def get_device_info_from_sda_fabric(deviceManagementIpAddress: str) -> Optional[Dict[str, Any]]:
    """Get device info from SDA Fabric

    Args:
        deviceManagementIpAddress: deviceManagementIpAddress
    """
    global client
    if not client:
        return {"error": "Not connected. Use connect() first."}

    kwargs = {}
    params = {}
    if deviceManagementIpAddress is not None:
        params['deviceManagementIpAddress'] = deviceManagementIpAddress
    if params:
        kwargs['params'] = params
    return await client.request('GET', f'/dna/intent/api/v1/business/sda/device', **kwargs)

@mcp.tool()
async def add_ip_pool_in_sda_virtual_network(request_body: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Add IP Pool in SDA Virtual Network

    Args:
        request_body: Request body data
    """
    global client
    if not client:
        return {"error": "Not connected. Use connect() first."}

    kwargs = {}
    kwargs['json'] = request_body
    return await client.request('POST', f'/dna/intent/api/v1/business/sda/virtualnetwork/ippool', **kwargs)

@mcp.tool()
async def delete_ip_pool_from_sda_virtual_network(siteNameHierarchy: str, virtualNetworkName: str, ipPoolName: str) -> Optional[Dict[str, Any]]:
    """Delete IP Pool from SDA Virtual Network

    Args:
        siteNameHierarchy: siteNameHierarchy
        virtualNetworkName: virtualNetworkName
        ipPoolName: ipPoolName
    """
    global client
    if not client:
        return {"error": "Not connected. Use connect() first."}

    kwargs = {}
    params = {}
    if siteNameHierarchy is not None:
        params['siteNameHierarchy'] = siteNameHierarchy
    if virtualNetworkName is not None:
        params['virtualNetworkName'] = virtualNetworkName
    if ipPoolName is not None:
        params['ipPoolName'] = ipPoolName
    if params:
        kwargs['params'] = params
    return await client.request('DELETE', f'/dna/intent/api/v1/business/sda/virtualnetwork/ippool', **kwargs)

@mcp.tool()
async def get_ip_pool_from_sda_virtual_network(siteNameHierarchy: str, virtualNetworkName: str, ipPoolName: str) -> Optional[Dict[str, Any]]:
    """Get IP Pool from SDA Virtual Network

    Args:
        siteNameHierarchy: siteNameHierarchy
        virtualNetworkName: virtualNetworkName
        ipPoolName: ipPoolName. Note: Use vlanName as a value for this parameter if same ip pool is assigned to multiple virtual networks (e.g.. ipPoolName=vlan1021)
    """
    global client
    if not client:
        return {"error": "Not connected. Use connect() first."}

    kwargs = {}
    params = {}
    if siteNameHierarchy is not None:
        params['siteNameHierarchy'] = siteNameHierarchy
    if virtualNetworkName is not None:
        params['virtualNetworkName'] = virtualNetworkName
    if ipPoolName is not None:
        params['ipPoolName'] = ipPoolName
    if params:
        kwargs['params'] = params
    return await client.request('GET', f'/dna/intent/api/v1/business/sda/virtualnetwork/ippool', **kwargs)

@mcp.tool()
async def get_site_from_sda_fabric(siteNameHierarchy: str) -> Optional[Dict[str, Any]]:
    """Get Site from SDA Fabric

    Get Site info from SDA Fabric

    Args:
        siteNameHierarchy: Site Name Hierarchy
    """
    global client
    if not client:
        return {"error": "Not connected. Use connect() first."}

    kwargs = {}
    params = {}
    if siteNameHierarchy is not None:
        params['siteNameHierarchy'] = siteNameHierarchy
    if params:
        kwargs['params'] = params
    return await client.request('GET', f'/dna/intent/api/v1/business/sda/fabric-site', **kwargs)

@mcp.tool()
async def add_site_in_sda_fabric(request_body: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Add Site in SDA Fabric

    Args:
        request_body: Request body data
    """
    global client
    if not client:
        return {"error": "Not connected. Use connect() first."}

    kwargs = {}
    kwargs['json'] = request_body
    return await client.request('POST', f'/dna/intent/api/v1/business/sda/fabric-site', **kwargs)

@mcp.tool()
async def get_multicast_details_from_sda_fabric(siteNameHierarchy: str) -> Optional[Dict[str, Any]]:
    """Get multicast details from SDA fabric

    Args:
        siteNameHierarchy: fabric site name hierarchy
    """
    global client
    if not client:
        return {"error": "Not connected. Use connect() first."}

    kwargs = {}
    params = {}
    if siteNameHierarchy is not None:
        params['siteNameHierarchy'] = siteNameHierarchy
    if params:
        kwargs['params'] = params
    return await client.request('GET', f'/dna/intent/api/v1/business/sda/multicast', **kwargs)

@mcp.tool()
async def add_vn_in_fabric(request_body: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Add VN in fabric

    Add virtual network (VN) in SDA Fabric

    Args:
        request_body: Request body data
    """
    global client
    if not client:
        return {"error": "Not connected. Use connect() first."}

    kwargs = {}
    kwargs['json'] = request_body
    return await client.request('POST', f'/dna/intent/api/v1/business/sda/virtual-network', **kwargs)

@mcp.tool()
async def get_vn_from_sda_fabric(virtualNetworkName: str, siteNameHierarchy: str) -> Optional[Dict[str, Any]]:
    """Get VN from SDA Fabric

    Get virtual network (VN) from SDA Fabric

    Args:
        virtualNetworkName: virtualNetworkName
        siteNameHierarchy: siteNameHierarchy
    """
    global client
    if not client:
        return {"error": "Not connected. Use connect() first."}

    kwargs = {}
    params = {}
    if virtualNetworkName is not None:
        params['virtualNetworkName'] = virtualNetworkName
    if siteNameHierarchy is not None:
        params['siteNameHierarchy'] = siteNameHierarchy
    if params:
        kwargs['params'] = params
    return await client.request('GET', f'/dna/intent/api/v1/business/sda/virtual-network', **kwargs)

@mcp.tool()
async def delete_vn_from_sda_fabric(virtualNetworkName: str, siteNameHierarchy: str) -> Optional[Dict[str, Any]]:
    """Delete VN from SDA Fabric

    Delete virtual network (VN) from SDA Fabric

    Args:
        virtualNetworkName: virtualNetworkName
        siteNameHierarchy: siteNameHierarchy
    """
    global client
    if not client:
        return {"error": "Not connected. Use connect() first."}

    kwargs = {}
    params = {}
    if virtualNetworkName is not None:
        params['virtualNetworkName'] = virtualNetworkName
    if siteNameHierarchy is not None:
        params['siteNameHierarchy'] = siteNameHierarchy
    if params:
        kwargs['params'] = params
    return await client.request('DELETE', f'/dna/intent/api/v1/business/sda/virtual-network', **kwargs)

@mcp.tool()
async def re__provision_wired_device(request_body: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Re-Provision Wired Device

    Args:
        request_body: Request body data
    """
    global client
    if not client:
        return {"error": "Not connected. Use connect() first."}

    kwargs = {}
    kwargs['json'] = request_body
    return await client.request('PUT', f'/dna/intent/api/v1/business/sda/provision-device', **kwargs)

@mcp.tool()
async def provision_wired_device(request_body: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Provision Wired Device

    Args:
        request_body: Request body data
    """
    global client
    if not client:
        return {"error": "Not connected. Use connect() first."}

    kwargs = {}
    kwargs['json'] = request_body
    return await client.request('POST', f'/dna/intent/api/v1/business/sda/provision-device', **kwargs)

@mcp.tool()
async def get_provisioned_wired_device(deviceManagementIpAddress: str) -> Optional[Dict[str, Any]]:
    """Get Provisioned Wired Device

    Args:
        deviceManagementIpAddress: deviceManagementIpAddress
    """
    global client
    if not client:
        return {"error": "Not connected. Use connect() first."}

    kwargs = {}
    params = {}
    if deviceManagementIpAddress is not None:
        params['deviceManagementIpAddress'] = deviceManagementIpAddress
    if params:
        kwargs['params'] = params
    return await client.request('GET', f'/dna/intent/api/v1/business/sda/provision-device', **kwargs)

@mcp.tool()
async def get_virtual_network_summary(siteNameHierarchy: str) -> Optional[Dict[str, Any]]:
    """Get Virtual Network Summary

    Args:
        siteNameHierarchy: Complete fabric siteNameHierarchy Path
    """
    global client
    if not client:
        return {"error": "Not connected. Use connect() first."}

    kwargs = {}
    params = {}
    if siteNameHierarchy is not None:
        params['siteNameHierarchy'] = siteNameHierarchy
    if params:
        kwargs['params'] = params
    return await client.request('GET', f'/dna/intent/api/v1/business/sda/virtual-network/summary', **kwargs)

@mcp.tool()
async def add_port_assignment_for_user_device_in_sda_fabric(request_body: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Add Port assignment for user device in SDA Fabric

    Add Port assignment for user device in SDA Fabric.

    Args:
        request_body: Request body data
    """
    global client
    if not client:
        return {"error": "Not connected. Use connect() first."}

    kwargs = {}
    kwargs['json'] = request_body
    return await client.request('POST', f'/dna/intent/api/v1/business/sda/hostonboarding/user-device', **kwargs)


@mcp.tool()
async def get_port_assignment_for_user_device_in_sda_fabric(deviceManagementIpAddress: str, interfaceName: str) -> Optional[Dict[str, Any]]:
    """Get Port assignment for user device in SDA Fabric

    Get Port assignment for user device in SDA Fabric.

    Args:
        deviceManagementIpAddress: deviceManagementIpAddress
        interfaceName: interfaceName
    """
    global client
    if not client:
        return {"error": "Not connected. Use connect() first."}

    kwargs = {}
    params = {}
    if deviceManagementIpAddress is not None:
        params['deviceManagementIpAddress'] = deviceManagementIpAddress
    if interfaceName is not None:
        params['interfaceName'] = interfaceName
    if params:
        kwargs['params'] = params
    return await client.request('GET', f'/dna/intent/api/v1/business/sda/hostonboarding/user-device', **kwargs)

@mcp.tool()
async def get_control_plane_device_from_sda_fabric(deviceManagementIpAddress: str) -> Optional[Dict[str, Any]]:
    """Get control plane device from SDA Fabric

    Args:
        deviceManagementIpAddress: deviceManagementIpAddress
    """
    global client
    if not client:
        return {"error": "Not connected. Use connect() first."}

    kwargs = {}
    params = {}
    if deviceManagementIpAddress is not None:
        params['deviceManagementIpAddress'] = deviceManagementIpAddress
    if params:
        kwargs['params'] = params
    return await client.request('GET', f'/dna/intent/api/v1/business/sda/control-plane-device', **kwargs)


@mcp.tool()
async def get_sites() -> str:
    """Get list of sites in the network."""
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

@mcp.tool()
async def get_network_devices(limit: int = 10, offset: int = 1) -> str:
    """Get list of network devices.

    Args:
        limit: Maximum number of devices to return (default: 10)
        offset: Pagination offset (default: 1)
    """
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


# Task Management Tools

def extract_task_id_from_response(response: Dict[str, Any]) -> Optional[str]:
    """Extract task ID from a typical Catalyst Center API response.

    Many POST operations return a response with either a taskId field or a URL containing the task ID.
    This helper function attempts to extract the task ID from various response formats.

    Args:
        response: The API response from a POST operation

    Returns:
        The task ID if found, None otherwise
    """
    if not response:
        return None

    # Check for direct taskId in response
    if 'response' in response:
        resp = response['response']

        # Check for taskId field
        if 'taskId' in resp:
            return resp['taskId']

        # Check for url field with task ID
        if 'url' in resp:
            url = resp['url']
            # Extract task ID from URL like "/api/v1/task/12345-..."
            if '/task/' in url:
                return url.split('/task/')[-1]

    # Check for taskId at top level
    if 'taskId' in response:
        return response['taskId']

    # Check for executionId (some APIs use this)
    if 'executionId' in response:
        return response['executionId']

    return None


@mcp.tool()
async def execute_and_monitor_task(
    operation_name: str,
    operation_func,
    *args,
    auto_wait: bool = True,
    max_wait_seconds: int = 300,
    **kwargs
) -> str:
    """Execute an operation and automatically monitor the resulting task.

    This is a helper function that can be used to wrap POST operations with automatic
    task monitoring. It executes the operation, extracts the task ID, and optionally
    waits for completion.

    Args:
        operation_name: Human-readable name of the operation
        operation_func: The function to execute (should return API response)
        auto_wait: Whether to automatically wait for task completion
        max_wait_seconds: Maximum time to wait if auto_wait is True
        *args, **kwargs: Arguments to pass to the operation function
    """
    global client
    if not client:
        return "Error: Not connected. Use connect() first."

    try:
        # Execute the operation
        print(f"Executing {operation_name}...")
        response = await operation_func(*args, **kwargs)

        if not response:
            return f"Error: {operation_name} failed - no response received"

        # Extract task ID
        task_id = extract_task_id_from_response(response)

        if not task_id:
            # Operation might have completed immediately or not be task-based
            return f"{operation_name} completed immediately. Response: {response}"

        result = f"{operation_name} initiated successfully.\nTask ID: {task_id}\n"

        if auto_wait:
            result += f"\nWaiting for completion (max {max_wait_seconds}s)...\n"
            completion_result = await wait_for_task_completion(task_id, max_wait_seconds)
            result += completion_result
        else:
            result += f"\nUse 'check task status for {task_id}' to monitor progress."

        return result

    except Exception as e:
        return f"Error executing {operation_name}: {str(e)}"


@mcp.tool()
async def get_task_by_id(task_id: str) -> Optional[Dict[str, Any]]:
    """Get task details by task ID

    Retrieves the details of a specific task using its task ID. This is useful for checking
    the status of operations that return a task ID (like most POST operations).

    Args:
        task_id: The unique identifier for the task
    """
    global client
    if not client:
        return {"error": "Not connected. Use connect() first."}

    kwargs = {}
    return await client.request('GET', f'/dna/intent/api/v1/task/{task_id}', **kwargs)


@mcp.tool()
async def get_tasks(
    offset: Optional[int] = None,
    limit: Optional[int] = None,
    status: Optional[str] = None,
    parent_id: Optional[str] = None,
    root_id: Optional[str] = None,
    start_time: Optional[int] = None,
    end_time: Optional[int] = None,
    sort_by: Optional[str] = None,
    order: Optional[str] = None
) -> Optional[Dict[str, Any]]:
    """Get tasks with filtering options

    Returns task(s) based on filter criteria. Useful for monitoring multiple tasks
    or finding tasks by status.

    Args:
        offset: The first record to show for this page (numbered from 1)
        limit: The number of records to show (min 1, max 500)
        status: Filter by task status (PENDING, FAILURE, SUCCESS)
        parent_id: Fetch tasks that have this parent ID
        root_id: Fetch tasks that have this root ID
        start_time: Epoch millisecond start time for task filtering
        end_time: Epoch millisecond end time for task filtering
        sort_by: Property to sort by
        order: Sort order (ascending or descending)
    """
    global client
    if not client:
        return {"error": "Not connected. Use connect() first."}

    params = {}
    if offset is not None:
        params['offset'] = offset
    if limit is not None:
        params['limit'] = limit
    if status is not None:
        params['status'] = status
    if parent_id is not None:
        params['parentId'] = parent_id
    if root_id is not None:
        params['rootId'] = root_id
    if start_time is not None:
        params['startTime'] = start_time
    if end_time is not None:
        params['endTime'] = end_time
    if sort_by is not None:
        params['sortBy'] = sort_by
    if order is not None:
        params['order'] = order

    kwargs = {}
    if params:
        kwargs['params'] = params

    return await client.request('GET', f'/dna/intent/api/v1/tasks', **kwargs)


@mcp.tool()
async def check_task_status(task_id: str) -> str:
    """Check the status of a task and return a human-readable summary

    This is a convenience function that gets task details and returns a formatted
    status summary including success/failure state, progress, and any error messages.

    Args:
        task_id: The unique identifier for the task
    """
    global client
    if not client:
        return "Error: Not connected. Use connect() first."

    task_response = await get_task_by_id(task_id)

    if not task_response or 'response' not in task_response:
        return f"Error: Could not retrieve task {task_id}"

    task = task_response['response']

    # Extract key information
    task_id_actual = task.get('id', 'Unknown')
    is_error = task.get('isError', False)
    progress = task.get('progress', 'Unknown')
    start_time = task.get('startTime', 0)
    end_time = task.get('endTime', 0)
    failure_reason = task.get('failureReason', '')
    error_code = task.get('errorCode', '')
    service_type = task.get('serviceType', 'Unknown')

    # Determine status
    if is_error:
        status = "FAILED"
    elif end_time > 0:
        status = "COMPLETED"
    else:
        status = "IN PROGRESS"

    # Format duration if available
    duration = ""
    if start_time > 0:
        if end_time > 0:
            duration_ms = end_time - start_time
            duration = f"Duration: {duration_ms/1000:.2f} seconds"
        else:
            duration = "Still running..."

    # Build status summary
    summary = f"""
Task Status Summary:
-------------------
Task ID: {task_id_actual}
Status: {status}
Service Type: {service_type}
Progress: {progress}
{duration}
"""

    if is_error and (failure_reason or error_code):
        summary += f"""
Error Details:
--------------"""
        if error_code:
            summary += f"\nError Code: {error_code}"
        if failure_reason:
            summary += f"\nFailure Reason: {failure_reason}"

    return summary.strip()


@mcp.tool()
async def wait_for_task_completion(
    task_id: str,
    max_wait_seconds: int = 300,
    check_interval_seconds: int = 5
) -> str:
    """Wait for a task to complete and return the final status

    Polls a task until it completes (success or failure) or until the maximum wait time is reached.

    Args:
        task_id: The unique identifier for the task
        max_wait_seconds: Maximum time to wait for completion (default: 300 seconds)
        check_interval_seconds: How often to check the task status (default: 5 seconds)
    """
    import asyncio
    import time

    global client
    if not client:
        return "Error: Not connected. Use connect() first."

    start_wait_time = time.time()
    max_wait_time = start_wait_time + max_wait_seconds

    while time.time() < max_wait_time:
        task_response = await get_task_by_id(task_id)

        if not task_response or 'response' not in task_response:
            return f"Error: Could not retrieve task {task_id}"

        task = task_response['response']
        is_error = task.get('isError', False)
        end_time = task.get('endTime', 0)

        # Check if task is complete
        if is_error or end_time > 0:
            elapsed_time = time.time() - start_wait_time
            status_summary = await check_task_status(task_id)
            return f"{status_summary}\n\nWait Time: {elapsed_time:.1f} seconds"

        # Wait before next check
        await asyncio.sleep(check_interval_seconds)

    # Timeout reached
    elapsed_time = time.time() - start_wait_time
    return f"Timeout: Task {task_id} did not complete within {max_wait_seconds} seconds (waited {elapsed_time:.1f}s)"


@mcp.tool()
async def get_recent_failed_tasks(limit: int = 10) -> str:
    """Get recent failed tasks for troubleshooting

    Retrieves the most recent failed tasks to help with troubleshooting operations.

    Args:
        limit: Maximum number of failed tasks to return (default: 10)
    """
    global client
    if not client:
        return "Error: Not connected. Use connect() first."

    # Get recent failed tasks
    tasks_response = await get_tasks(
        status="FAILURE",
        limit=limit,
        sort_by="startTime",
        order="desc"
    )

    if not tasks_response or 'response' not in tasks_response:
        return "No failed tasks found or error retrieving tasks."

    tasks = tasks_response['response']

    if not tasks:
        return "No recent failed tasks found."

    formatted_tasks = []
    for task in tasks:
        task_id = task.get('id', 'Unknown')
        service_type = task.get('serviceType', 'Unknown')
        failure_reason = task.get('failureReason', 'Unknown reason')
        error_code = task.get('errorCode', '')
        start_time = task.get('startTime', 0)

        # Convert timestamp to readable format
        import datetime
        if start_time > 0:
            dt = datetime.datetime.fromtimestamp(start_time / 1000)
            time_str = dt.strftime('%Y-%m-%d %H:%M:%S')
        else:
            time_str = 'Unknown'

        formatted = f"""
Task ID: {task_id}
Service: {service_type}
Time: {time_str}
Error Code: {error_code}
Reason: {failure_reason}
"""
        formatted_tasks.append(formatted.strip())

    return "Recent Failed Tasks:\n" + "\n---\n".join(formatted_tasks)


if __name__ == "__main__":
    import sys

    # Check if we should run as HTTP server (for testing/debugging)
    if len(sys.argv) > 1 and sys.argv[1] == "--http":
        import uvicorn
        # Run as HTTP server for testing
        uvicorn.run(mcp.app, host="0.0.0.0", port=8000)
    else:
        # Initialize and run the MCP server
        mcp.run(transport='stdio')
