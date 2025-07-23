from typing import Any, Dict, List, Optional

from client import client_manager
from mcp_instance import create_mcp_instance
from agents.base_agent import SmartDomainAgent, format_response, extract_parameters_from_query

agent = create_mcp_instance("DevicesAgent")

# Create smart domain agent wrapper for devices
devices_tool_keywords = {
    "connect": ["connect", "login", "auth", "authenticate"],
    "get_device_list": ["device", "devices", "inventory", "list devices", "network devices"],
    "get_device_by_id": ["device details", "device info", "specific device", "device id"],
    "delete_device_by_id": ["delete device", "remove device", "unregister device"],
    "add_device": ["add device", "register device", "discover device", "new device"],
    "update_device_details": ["update device", "modify device", "edit device"],
    "get_device_health": ["device health", "health status", "device performance"],
    "get_network_devices_count": ["device count", "number of devices", "total devices"],
    "get_planned_access_points_for_floor": ["access point", "ap", "wireless", "floor plan"],
    "update_health_score_definitions": ["health score", "health metrics", "performance metrics"],
    "get_network_device_interface_count": ["interface", "interfaces", "port count", "network interfaces"],
    "get_device_config_by_id": ["device config", "configuration", "device settings"],
    "update_interface_details": ["interface config", "port config", "interface settings"],
    "get_inventory_insight_device_link_mismatch": ["mismatch", "link mismatch", "inventory mismatch"],
    "get_resync_interval_for_the_network_device": ["resync", "sync interval", "device sync"],
    "update_resync_interval_for_the_network_device": ["update resync", "change sync interval"],
    "legit_operations_for_interface": ["interface operations", "valid operations", "allowed operations"],
    "get_the_details_of_physical_components_of_the_given_device": ["physical components", "hardware details", "device components"]
}

smart_agent = SmartDomainAgent("Devices", agent, devices_tool_keywords)


@agent.tool()
async def update_health_score_definitions(
    request_body: Dict[str, Any], x_caller_id: Optional[str] = None
) -> Optional[Dict[str, Any]]:
    """
    Update health score definitions.

    Args:
        request_body: The request body containing health score definition updates.
        x_caller_id: Optional caller ID to trace the origin of API calls.
    """
    client = client_manager.get_client()
    if not client:
        return {"error": "Not connected. Use connect() first."}

    kwargs = {"json": request_body}
    headers = {}
    if x_caller_id is not None:
        headers["X-CALLER-ID"] = x_caller_id
    if headers:
        kwargs["headers"] = headers

    return await client.request("POST", "/dna/intent/api/v1/healthScoreDefinitions/bulkUpdate", **kwargs)


@agent.tool()
async def delete_device_by_id(id: str, clean_config: Optional[bool] = None) -> Optional[Dict[str, Any]]:
    """
    Delete a non-provisioned network device by its ID.

    Args:
        id: The unique ID of the device to delete.
        clean_config: If true, attempts to remove settings configured during device addition.
    """
    client = client_manager.get_client()
    if not client:
        return {"error": "Not connected. Use connect() first."}

    kwargs = {}
    params = {}
    if clean_config is not None:
        params["cleanConfig"] = clean_config
    if params:
        kwargs["params"] = params

    return await client.request("DELETE", f"/dna/intent/api/v1/network-device/{id}", **kwargs)


@agent.tool()
async def get_device_by_id(id: str) -> Optional[Dict[str, Any]]:
    """
    Get network device details for a given device ID.

    Args:
        id: The unique ID of the device.
    """
    client = client_manager.get_client()
    if not client:
        return {"error": "Not connected. Use connect() first."}

    return await client.request("GET", f"/dna/intent/api/v1/network-device/{id}")


@agent.tool()
async def get_device_list(
    hostname: Optional[List[str]] = None,
    management_ip_address: Optional[List[str]] = None,
    mac_address: Optional[List[str]] = None,
    location_name: Optional[List[str]] = None,
    serial_number: Optional[List[str]] = None,
    location: Optional[List[str]] = None,
    family: Optional[List[str]] = None,
    type: Optional[List[str]] = None,
    series: Optional[List[str]] = None,
    collection_status: Optional[List[str]] = None,
    collection_interval: Optional[List[str]] = None,
    not_synced_for_minutes: Optional[List[str]] = None,
    error_code: Optional[List[str]] = None,
    error_description: Optional[List[str]] = None,
    software_version: Optional[List[str]] = None,
    software_type: Optional[List[str]] = None,
    platform_id: Optional[List[str]] = None,
    role: Optional[List[str]] = None,
    reachability_status: Optional[List[str]] = None,
    up_time: Optional[List[str]] = None,
    associated_wlc_ip: Optional[List[str]] = None,
    license_name: Optional[List[str]] = None,
    license_type: Optional[List[str]] = None,
    license_status: Optional[List[str]] = None,
    module_name: Optional[List[str]] = None,
    module_equpimenttype: Optional[List[str]] = None,
    module_service_state: Optional[List[str]] = None,
    module_vendor_equipment_type: Optional[List[str]] = None,
    module_part_number: Optional[List[str]] = None,
    module_operation_state_code: Optional[List[str]] = None,
    id: Optional[str] = None,
    device_support_level: Optional[str] = None,
    offset: Optional[int] = None,
    limit: Optional[int] = None,
) -> Optional[Dict[str, Any]]:
    """
    Get a list of network devices based on filter criteria.

    Args:
        hostname: Filter by device hostname.
        management_ip_address: Filter by management IP address.
        mac_address: Filter by MAC address.
        location_name: Filter by location name.
        serial_number: Filter by serial number.
        location: Filter by location.
        family: Filter by device family.
        type: Filter by device type.
        series: Filter by device series.
        collection_status: Filter by collection status.
        collection_interval: Filter by collection interval.
        not_synced_for_minutes: Filter by devices not synced for a number of minutes.
        error_code: Filter by error code.
        error_description: Filter by error description.
        software_version: Filter by software version.
        software_type: Filter by software type.
        platform_id: Filter by platform ID.
        role: Filter by device role.
        reachability_status: Filter by reachability status.
        up_time: Filter by uptime.
        associated_wlc_ip: Filter by associated WLC IP.
        license_name: Filter by license name.
        license_type: Filter by license type.
        license_status: Filter by license status.
        module_name: Filter by module name.
        module_equpimenttype: Filter by module equipment type.
        module_service_state: Filter by module service state.
        module_vendor_equipment_type: Filter by module vendor equipment type.
        module_part_number: Filter by module part number.
        module_operation_state_code: Filter by module operation state code.
        id: A comma-separated list of device IDs to retrieve.
        device_support_level: Filter by device support level.
        offset: Starting record index for pagination.
        limit: Number of records to return per page (max 500).
    """
    client = client_manager.get_client()
    if not client:
        return {"error": "Not connected. Use connect() first."}

    kwargs = {}
    params = {}
    if hostname is not None:
        params["hostname"] = hostname
    if management_ip_address is not None:
        params["managementIpAddress"] = management_ip_address
    if mac_address is not None:
        params["macAddress"] = mac_address
    if location_name is not None:
        params["locationName"] = location_name
    if serial_number is not None:
        params["serialNumber"] = serial_number
    if location is not None:
        params["location"] = location
    if family is not None:
        params["family"] = family
    if type is not None:
        params["type"] = type
    if series is not None:
        params["series"] = series
    if collection_status is not None:
        params["collectionStatus"] = collection_status
    if collection_interval is not None:
        params["collectionInterval"] = collection_interval
    if not_synced_for_minutes is not None:
        params["notSyncedForMinutes"] = not_synced_for_minutes
    if error_code is not None:
        params["errorCode"] = error_code
    if error_description is not None:
        params["errorDescription"] = error_description
    if software_version is not None:
        params["softwareVersion"] = software_version
    if software_type is not None:
        params["softwareType"] = software_type
    if platform_id is not None:
        params["platformId"] = platform_id
    if role is not None:
        params["role"] = role
    if reachability_status is not None:
        params["reachabilityStatus"] = reachability_status
    if up_time is not None:
        params["upTime"] = up_time
    if associated_wlc_ip is not None:
        params["associatedWlcIp"] = associated_wlc_ip
    if license_name is not None:
        params["license.name"] = license_name
    if license_type is not None:
        params["license.type"] = license_type
    if license_status is not None:
        params["license.status"] = license_status
    if module_name is not None:
        params["module+name"] = module_name
    if module_equpimenttype is not None:
        params["module+equpimenttype"] = module_equpimenttype
    if module_service_state is not None:
        params["module+servicestate"] = module_service_state
    if module_vendor_equipment_type is not None:
        params["module+vendorequipmenttype"] = module_vendor_equipment_type
    if module_part_number is not None:
        params["module+partnumber"] = module_part_number
    if module_operation_state_code is not None:
        params["module+operationstatecode"] = module_operation_state_code
    if id is not None:
        params["id"] = id
    if device_support_level is not None:
        params["deviceSupportLevel"] = device_support_level
    if offset is not None:
        params["offset"] = offset
    if limit is not None:
        params["limit"] = limit
    if params:
        kwargs["params"] = params

    return await client.request("GET", "/dna/intent/api/v1/network-device", **kwargs)


@agent.tool()
async def add_device(request_body: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """
    Add a device to the inventory using its credentials.

    Args:
        request_body: The request body containing device information and credentials.
    """
    client = client_manager.get_client()
    if not client:
        return {"error": "Not connected. Use connect() first."}

    kwargs = {"json": request_body}
    return await client.request("POST", "/dna/intent/api/v1/network-device", **kwargs)


@agent.tool()
async def update_device_details(request_body: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """
    Update details for one or more devices and trigger an inventory sync.

    Args:
        request_body: The request body containing device updates like credentials or management IP.
    """
    client = client_manager.get_client()
    if not client:
        return {"error": "Not connected. Use connect() first."}

    kwargs = {"json": request_body}
    return await client.request("PUT", "/dna/intent/api/v1/network-device", **kwargs)


@agent.tool()
async def update_global_resync_interval(request_body: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """
    Update the global resync interval for devices without a custom interval.

    Args:
        request_body: The request body containing the new interval in minutes.
    """
    client = client_manager.get_client()
    if not client:
        return {"error": "Not connected. Use connect() first."}

    kwargs = {"json": request_body}
    return await client.request("PUT", "/dna/intent/api/v1/networkDevices/resyncIntervalSettings", **kwargs)


@agent.tool()
async def get_network_devices_count(request_body: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """
    Get the total number of Network Devices based on complex filters.

    Args:
        request_body: The request body containing filters and aggregation functions.
    """
    client = client_manager.get_client()
    if not client:
        return {"error": "Not connected. Use connect() first."}

    kwargs = {"json": request_body}
    return await client.request("POST", "/dna/data/api/v1/networkDevices/query/count", **kwargs)


@agent.tool()
async def update_planned_access_point_for_floor(
    floor_id: str, request_body: Dict[str, Any]
) -> Optional[Dict[str, Any]]:
    """
    Update a planned access point on an existing floor map.

    Args:
        floor_id: The instance UUID of the floor.
        request_body: The request body containing the updated access point details.
    """
    client = client_manager.get_client()
    if not client:
        return {"error": "Not connected. Use connect() first."}

    kwargs = {"json": request_body}
    return await client.request(
        "PUT",
        f"/dna/intent/api/v1/floors/{floor_id}/planned-access-points",
        **kwargs,
    )


@agent.tool()
async def get_planned_access_points_for_floor(
    floor_id: str,
    limit: Optional[int] = None,
    offset: Optional[int] = None,
    radios: Optional[bool] = None,
) -> Optional[Dict[str, Any]]:
    """
    Get a list of Planned Access Points for a specific floor.

    Args:
        floor_id: The instance UUID of the floor.
        limit: The number of records to return (max 500).
        offset: The page offset for pagination.
        radios: If true, includes planned radio details in the response.
    """
    client = client_manager.get_client()
    if not client:
        return {"error": "Not connected. Use connect() first."}

    kwargs = {}
    params = {}
    if limit is not None:
        params["limit"] = limit
    if offset is not None:
        params["offset"] = offset
    if radios is not None:
        params["radios"] = radios
    if params:
        kwargs["params"] = params

    return await client.request(
        "GET",
        f"/dna/intent/api/v1/floors/{floor_id}/planned-access-points",
        **kwargs,
    )


@agent.tool()
async def create_planned_access_point_for_floor(
    floor_id: str, request_body: Dict[str, Any]
) -> Optional[Dict[str, Any]]:
    """
    Create a new planned access point on an existing floor map.

    Args:
        floor_id: The instance UUID of the floor.
        request_body: The request body containing the new access point details.
    """
    client = client_manager.get_client()
    if not client:
        return {"error": "Not connected. Use connect() first."}

    kwargs = {"json": request_body}
    return await client.request(
        "POST",
        f"/dna/intent/api/v1/floors/{floor_id}/planned-access-points",
        **kwargs,
    )


@agent.tool()
async def get_device_health(
    device_role: Optional[str] = None,
    site_id: Optional[str] = None,
    health: Optional[str] = None,
    start_time: Optional[int] = None,
    end_time: Optional[int] = None,
    limit: Optional[int] = None,
    offset: Optional[int] = None,
) -> Optional[Dict[str, Any]]:
    """
    Get device health information from DNA Assurance.

    Args:
        device_role: Filter by device role (e.g., CORE, ACCESS, WLC, AP).
        site_id: Filter by DNA Center site UUID.
        health: Filter by health category (e.g., POOR, FAIR, GOOD).
        start_time: Start time in UTC epoch milliseconds.
        end_time: End time in UTC epoch milliseconds.
        limit: Maximum number of devices to return (default 50, max 500).
        offset: The starting offset for pagination.
    """
    client = client_manager.get_client()
    if not client:
        return {"error": "Not connected. Use connect() first."}

    kwargs = {}
    params = {}
    if device_role is not None:
        params["deviceRole"] = device_role
    if site_id is not None:
        params["siteId"] = site_id
    if health is not None:
        params["health"] = health
    if start_time is not None:
        params["startTime"] = start_time
    if end_time is not None:
        params["endTime"] = end_time
    if limit is not None:
        params["limit"] = limit
    if offset is not None:
        params["offset"] = offset
    if params:
        kwargs["params"] = params

    return await client.request("GET", "/dna/intent/api/v1/device-health", **kwargs)


@agent.tool()
async def get_network_device_interface_count(
    start_time: Optional[int] = None,
    end_time: Optional[int] = None,
    site_hierarchy: Optional[str] = None,
    site_hierarchy_id: Optional[str] = None,
    site_id: Optional[str] = None,
    network_device_id: Optional[str] = None,
    network_device_ip_address: Optional[str] = None,
    network_device_mac_address: Optional[str] = None,
    interface_id: Optional[str] = None,
    interface_name: Optional[str] = None,
) -> Optional[Dict[str, Any]]:
    """
    Get the total count of network device interfaces within a time range or the latest count.

    Args:
        start_time: Start time in UNIX epoch milliseconds.
        end_time: End time in UNIX epoch milliseconds.
        site_hierarchy: Filter by full site hierarchy path (e.g., Global/Area/Building).
        site_hierarchy_id: Filter by full site hierarchy UUID path.
        site_id: Filter by site UUID.
        network_device_id: Filter by network device UUID(s).
        network_device_ip_address: Filter by network device IP address(es).
        network_device_mac_address: Filter by network device MAC address(es).
        interface_id: Filter by interface UUID(s).
        interface_name: Filter by interface name(s).
    """
    client = client_manager.get_client()
    if not client:
        return {"error": "Not connected. Use connect() first."}

    kwargs = {}
    params = {}
    if start_time is not None:
        params["startTime"] = start_time
    if end_time is not None:
        params["endTime"] = end_time
    if site_hierarchy is not None:
        params["siteHierarchy"] = site_hierarchy
    if site_hierarchy_id is not None:
        params["siteHierarchyId"] = site_hierarchy_id
    if site_id is not None:
        params["siteId"] = site_id
    if network_device_id is not None:
        params["networkDeviceId"] = network_device_id
    if network_device_ip_address is not None:
        params["networkDeviceIpAddress"] = network_device_ip_address
    if network_device_mac_address is not None:
        params["networkDeviceMacAddress"] = network_device_mac_address
    if interface_id is not None:
        params["interfaceId"] = interface_id
    if interface_name is not None:
        params["interfaceName"] = interface_name
    if params:
        kwargs["params"] = params

    return await client.request("GET", "/dna/data/api/v1/interfaces/count", **kwargs)


@agent.tool()
async def delete_network_device_with_cleanup(request_body: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """
    Delete a network device after performing configuration cleanup on it.

    Args:
        request_body: The request body containing the device ID to be deleted.
    """
    client = client_manager.get_client()
    if not client:
        return {"error": "Not connected. Use connect() first."}

    kwargs = {"json": request_body}
    return await client.request("POST", "/dna/intent/api/v1/networkDevices/deleteWithCleanup", **kwargs)


@agent.tool()
async def get_inventory_insight_device_link_mismatch(
    site_id: str,
    category: str,
    offset: Optional[int] = None,
    limit: Optional[int] = None,
    sort_by: Optional[str] = None,
    order: Optional[str] = None,
) -> Optional[Dict[str, Any]]:
    """
    Find all devices within a site that have a link mismatch (speed/duplex or vlan).

    Args:
        site_id: The ID of the site to search within.
        category: The mismatch category. Must be 'speed-duplex' or 'vlan'.
        offset: Starting record index for pagination. Default is 1.
        limit: Number of records to return per page (max 500).
        sort_by: The field to sort the results by.
        order: The sort order, 'asc' or 'desc'. Default is 'asc'.
    """
    client = client_manager.get_client()
    if not client:
        return {"error": "Not connected. Use connect() first."}

    kwargs = {}
    params = {"category": category}
    if offset is not None:
        params["offset"] = offset
    if limit is not None:
        params["limit"] = limit
    if sort_by is not None:
        params["sortBy"] = sort_by
    if order is not None:
        params["order"] = order
    if params:
        kwargs["params"] = params

    return await client.request(
        "GET",
        f"/dna/intent/api/v1/network-device/insight/{site_id}/device-link",
        **kwargs,
    )

from typing import Any, Dict, Optional

from client import client_manager
from mcp_instance import create_mcp_instance

agent = create_mcp_instance("DevicesAgent")


@agent.tool()
async def count_the_number_of_network_devices_with_filters(
    request_body: Dict[str, Any]
) -> Optional[Dict[str, Any]]:
    """
    Count the number of network devices with filters.

    Args:
        request_body: The request body containing the filter query.
    """
    client = client_manager.get_client()
    if not client:
        return {"error": "Not connected. Use connect() first."}

    kwargs = {"json": request_body}
    return await client.request(
        "POST", "/dna/intent/api/v1/networkDevices/query/count", **kwargs
    )


@agent.tool()
async def get_the_details_of_physical_components_of_the_given_device(
    deviceUuid: str, type: Optional[str] = None
) -> Optional[Dict[str, Any]]:
    """
    Get the Details of Physical Components of the Given Device.

    Args:
        deviceUuid: The unique identifier (UUID) of the device.
        type: The type of equipment to fetch (e.g., PowerSupply, Fan, Chassis). If omitted, all equipment is returned.
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

    return await client.request(
        "GET", f"/dna/intent/api/v1/network-device/{deviceUuid}/equipment", **kwargs
    )


@agent.tool()
async def get_device_config_by_id(
    networkDeviceId: str,
) -> Optional[Dict[str, Any]]:
    """
    Get Device Config by Id.

    Args:
        networkDeviceId: The unique identifier of the network device.
    """
    client = client_manager.get_client()
    if not client:
        return {"error": "Not connected. Use connect() first."}

    return await client.request(
        "GET", f"/dna/intent/api/v1/network-device/{networkDeviceId}/config"
    )


@agent.tool()
async def update_interface_details(
    interfaceUuid: str,
    request_body: Dict[str, Any],
    deploymentMode: Optional[str] = None,
) -> Optional[Dict[str, Any]]:
    """
    Update Interface details.

    Args:
        interfaceUuid: The unique identifier (UUID) of the interface.
        request_body: The request body containing updates for description, VLAN, admin status, etc.
        deploymentMode: Set to 'Preview' to see changes without pushing, or 'Deploy' to push to the device.
    """
    client = client_manager.get_client()
    if not client:
        return {"error": "Not connected. Use connect() first."}

    kwargs = {"json": request_body}
    params = {}
    if deploymentMode is not None:
        params["deploymentMode"] = deploymentMode
    if params:
        kwargs["params"] = params

    return await client.request(
        "PUT", f"/dna/intent/api/v1/interface/{interfaceUuid}", **kwargs
    )


@agent.tool()
async def get_resync_interval_for_the_network_device(
    id: str,
) -> Optional[Dict[str, Any]]:
    """
    Get resync interval for the network device.

    Args:
        id: The unique identifier of the network device.
    """
    client = client_manager.get_client()
    if not client:
        return {"error": "Not connected. Use connect() first."}

    return await client.request(
        "GET", f"/dna/intent/api/v1/networkDevices/{id}/resyncIntervalSettings"
    )


@agent.tool()
async def update_resync_interval_for_the_network_device(
    id: str, request_body: Dict[str, Any]
) -> Optional[Dict[str, Any]]:
    """
    Update resync interval for the network device.

    Args:
        id: The unique identifier of the network device.
        request_body: The request body containing the new interval. Set to 0 to disable, or null to use global settings.
    """
    client = client_manager.get_client()
    if not client:
        return {"error": "Not connected. Use connect() first."}

    kwargs = {"json": request_body}
    return await client.request(
        "PUT",
        f"/dna/intent/api/v1/networkDevices/{id}/resyncIntervalSettings",
        **kwargs,
    )


@agent.tool()
async def legit_operations_for_interface(
    interfaceUuid: str,
) -> Optional[Dict[str, Any]]:
    """
    Legit operations for interface.

    Args:
        interfaceUuid: The unique identifier (UUID) of the interface.
    """
    client = client_manager.get_client()
    if not client:
        return {"error": "Not connected. Use connect() first."}

    return await client.request(
        "GET", f"/dna/intent/api/v1/interface/{interfaceUuid}/legit-operation"
    )


@agent.tool()
async def get_device_config_count() -> Optional[Dict[str, Any]]:
    """
    Get Device Config Count.
    """
    client = client_manager.get_client()
    if not client:
        return {"error": "Not connected. Use connect() first."}

    return await client.request("GET", "/dna/intent/api/v1/network-device/config/count")


@agent.tool()
async def retrieves_the_total_number_of_dhcp_services_for_given_set_of_complex_filters(
    request_body: Dict[str, Any], x_caller_id: Optional[str] = None
) -> Optional[Dict[str, Any]]:
    """
    Retrieves the total number of DHCP Services for given set of complex filters.

    Args:
        request_body: The request body containing complex filters for the query.
        x_caller_id: Optional caller ID to trace the origin of API calls.
    """
    client = client_manager.get_client()
    if not client:
        return {"error": "Not connected. Use connect() first."}

    kwargs = {"json": request_body}
    headers = {}
    if x_caller_id is not None:
        headers["X-CALLER-ID"] = x_caller_id
    if headers:
        kwargs["headers"] = headers

    return await client.request(
        "POST", "/dna/data/api/v1/dhcpServices/query/count", **kwargs
    )


@agent.tool()
async def get_device_interface_vlans(
    id: str, interfaceType: Optional[str] = None
) -> Optional[Dict[str, Any]]:
    """
    Get Device Interface VLANs.

    Args:
        id: The unique identifier (UUID) of the device.
        interfaceType: The type of interface to query for VLANs.
    """
    client = client_manager.get_client()
    if not client:
        return {"error": "Not connected. Use connect() first."}

    kwargs = {}
    params = {}
    if interfaceType is not None:
        params["interfaceType"] = interfaceType
    if params:
        kwargs["params"] = params

    return await client.request(
        "GET", f"/dna/intent/api/v1/network-device/{id}/vlan", **kwargs
    )


@agent.tool()
async def get_details_of_a_single_network_device(
    id: str, views: Optional[str] = None
) -> Optional[Dict[str, Any]]:
    """
    Get details of a single network device.

    Args:
        id: The unique identifier for the network device.
        views: Specific views to fetch (e.g., BASIC, RESYNC, USER_DEFINED_FIELDS). Comma-separated for multiple.
    """
    client = client_manager.get_client()
    if not client:
        return {"error": "Not connected. Use connect() first."}

    kwargs = {}
    params = {}
    if views is not None:
        params["views"] = views
    if params:
        kwargs["params"] = params

    return await client.request(
        "GET", f"/dna/intent/api/v1/networkDevices/{id}", **kwargs
    )


# Register all tools with the smart agent
def register_devices_tools():
    """Register all device tools with the smart domain agent."""
    # Get all functions that are decorated with @agent.tool()
    import inspect
    current_module = inspect.getmodule(inspect.currentframe())
    
    for name, obj in inspect.getmembers(current_module):
        if (inspect.iscoroutinefunction(obj) and 
            hasattr(obj, '__name__') and 
            not name.startswith('_') and
            name not in ['register_devices_tools', 'process_request']):
            smart_agent.register_tool(name, obj)


# Process request method for the devices agent
async def process_request(query: str) -> str:
    """
    Process device-related requests with intelligent routing.
    """
    return await smart_agent.process_request(query)

# Call registration on module load
register_devices_tools()

# Expose process_request at module level for router access
agent.process_request = process_request
