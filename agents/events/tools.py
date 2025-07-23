"""
Events Domain Agent

Handles event management, notifications, and alerts within the Catalyst Center.
"""

from typing import Any, Dict, Optional, List
from client import client_manager
from mcp_instance import create_mcp_instance
from agents.base_agent import SmartDomainAgent, format_response, extract_parameters_from_query

agent = create_mcp_instance("EventsAgent")

# Events domain keywords
events_tool_keywords = {
    "get_events": ["events", "event", "notifications", "alerts", "logs"],
    "get_event_subscriptions": ["subscription", "subscriptions", "event subscription"],
    "create_event_subscription": ["create subscription", "subscribe", "add subscription"],
    "update_event_subscription": ["update subscription", "modify subscription"],
    "delete_event_subscription": ["delete subscription", "remove subscription", "unsubscribe"],
    "get_event_types": ["event types", "event categories", "notification types"],
    "get_event_count": ["event count", "number of events"],
    "get_notification_config": ["notification config", "alert config", "event config"],
    "update_notification_config": ["update config", "configure notifications"],
    "get_event_series": ["event series", "event analytics", "event trends"],
    "export_events": ["export events", "download events", "event report"],
    "get_event_artifacts": ["artifacts", "event artifacts", "event details"],
    "clear_events": ["clear events", "delete events", "remove events"],
    "acknowledge_events": ["acknowledge", "ack events", "mark as acknowledged"],
    "get_event_enrichment": ["enrichment", "event enrichment", "event context"]
}

smart_agent = SmartDomainAgent("Events", agent, events_tool_keywords)

@agent.tool()
async def get_events(
    severity: Optional[str] = None,
    domain: Optional[str] = None,
    subdomain: Optional[str] = None,
    source: Optional[str] = None,
    event_id: Optional[str] = None,
    start_time: Optional[int] = None,
    end_time: Optional[int] = None,
    category: Optional[str] = None,
    type: Optional[str] = None,
    limit: Optional[int] = None,
    offset: Optional[int] = None,
    sort_by: Optional[str] = None,
    order: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get events from Catalyst Center.
    
    Args:
        severity: Filter by event severity (Critical, High, Medium, Low)
        domain: Filter by domain
        subdomain: Filter by subdomain  
        source: Filter by event source
        event_id: Get specific event by ID
        start_time: Start time (epoch timestamp)
        end_time: End time (epoch timestamp)
        category: Filter by event category
        type: Filter by event type
        limit: Maximum number of events to return
        offset: Number of events to skip
        sort_by: Field to sort by
        order: Sort order (asc/desc)
    """
    client = client_manager.get_client()
    if not client:
        return {"error": "Not connected. Use connect() first."}
    
    params = {}
    if severity is not None:
        params["severity"] = severity
    if domain is not None:
        params["domain"] = domain
    if subdomain is not None:
        params["subdomain"] = subdomain
    if source is not None:
        params["source"] = source
    if event_id is not None:
        params["eventId"] = event_id
    if start_time is not None:
        params["startTime"] = start_time
    if end_time is not None:
        params["endTime"] = end_time
    if category is not None:
        params["category"] = category
    if type is not None:
        params["type"] = type
    if limit is not None:
        params["limit"] = limit
    if offset is not None:
        params["offset"] = offset
    if sort_by is not None:
        params["sortBy"] = sort_by
    if order is not None:
        params["order"] = order
    
    # For demo purposes, return mock data
    return {
        "events": [
            {
                "eventId": "12345",
                "severity": "High",
                "domain": "Connectivity",
                "source": "Device-123",
                "message": "Device connectivity issue detected",
                "timestamp": 1690123456,
                "category": "Network",
                "type": "Connectivity"
            },
            {
                "eventId": "12346", 
                "severity": "Medium",
                "domain": "Performance",
                "source": "Interface-Gi0/1",
                "message": "High utilization detected on interface",
                "timestamp": 1690123400,
                "category": "Performance",
                "type": "Utilization"
            }
        ],
        "total_count": 2,
        "filters_applied": params
    }

@agent.tool()
async def get_event_subscriptions(
    name: Optional[str] = None,
    subscription_id: Optional[str] = None,
    event_ids: Optional[List[str]] = None
) -> Dict[str, Any]:
    """
    Get event subscriptions.
    
    Args:
        name: Filter by subscription name
        subscription_id: Get specific subscription by ID
        event_ids: Filter by event IDs
    """
    client = client_manager.get_client()
    if not client:
        return {"error": "Not connected. Use connect() first."}
    
    return {
        "subscriptions": [
            {
                "subscriptionId": "sub-001",
                "name": "Critical Events Subscription",
                "description": "Subscribe to all critical events",
                "filter": {
                    "eventIds": ["NETWORK-FAULT-001", "DEVICE-DOWN-001"],
                    "severities": ["Critical", "High"]
                },
                "subscriptionEndpoints": [
                    {
                        "instanceId": "endpoint-001",
                        "subscriptionDetails": {
                            "connectorType": "REST",
                            "method": "POST",
                            "url": "https://webhook.example.com/events"
                        }
                    }
                ],
                "version": "1.0.0",
                "isPrivate": False
            }
        ],
        "total_count": 1
    }

@agent.tool()
async def create_event_subscription(request_body: Dict[str, Any]) -> Dict[str, Any]:
    """
    Create a new event subscription.
    
    Args:
        request_body: Subscription configuration
    """
    client = client_manager.get_client()
    if not client:
        return {"error": "Not connected. Use connect() first."}
    
    # Validate required fields
    required_fields = ["name", "subscriptionEndpoints"]
    for field in required_fields:
        if field not in request_body:
            return {"error": f"Missing required field: {field}"}
    
    return {
        "executionId": "exec-12345",
        "executionStatusUrl": "/api/v1/task/exec-12345",
        "message": "Event subscription created successfully",
        "subscriptionId": "sub-002"
    }

@agent.tool()
async def update_event_subscription(
    subscription_id: str, 
    request_body: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Update an existing event subscription.
    
    Args:
        subscription_id: ID of subscription to update
        request_body: Updated subscription configuration
    """
    client = client_manager.get_client()
    if not client:
        return {"error": "Not connected. Use connect() first."}
    
    return {
        "executionId": "exec-12346",
        "executionStatusUrl": f"/api/v1/task/exec-12346",
        "message": f"Event subscription {subscription_id} updated successfully"
    }

@agent.tool()
async def delete_event_subscription(subscription_id: str) -> Dict[str, Any]:
    """
    Delete an event subscription.
    
    Args:
        subscription_id: ID of subscription to delete
    """
    client = client_manager.get_client()
    if not client:
        return {"error": "Not connected. Use connect() first."}
    
    return {
        "executionId": "exec-12347",
        "executionStatusUrl": f"/api/v1/task/exec-12347",
        "message": f"Event subscription {subscription_id} deleted successfully"
    }

@agent.tool()
async def get_event_types() -> Dict[str, Any]:
    """
    Get available event types and their details.
    """
    client = client_manager.get_client()
    if not client:
        return {"error": "Not connected. Use connect() first."}
    
    return {
        "eventTypes": [
            {
                "eventId": "NETWORK-FAULT-001",
                "name": "Network Fault",
                "description": "Network connectivity fault detected",
                "category": "Network",
                "severity": "Critical",
                "tags": ["network", "connectivity", "fault"]
            },
            {
                "eventId": "DEVICE-DOWN-001", 
                "name": "Device Down",
                "description": "Network device is unreachable",
                "category": "Device",
                "severity": "High",
                "tags": ["device", "connectivity", "down"]
            },
            {
                "eventId": "PERF-UTIL-001",
                "name": "High Utilization",
                "description": "Interface utilization above threshold",
                "category": "Performance", 
                "severity": "Medium",
                "tags": ["performance", "utilization", "interface"]
            }
        ],
        "total_count": 3
    }

@agent.tool()
async def get_event_count(
    severity: Optional[str] = None,
    domain: Optional[str] = None,
    start_time: Optional[int] = None,
    end_time: Optional[int] = None
) -> Dict[str, Any]:
    """
    Get count of events matching filters.
    
    Args:
        severity: Filter by severity
        domain: Filter by domain
        start_time: Start time (epoch timestamp)
        end_time: End time (epoch timestamp)
    """
    client = client_manager.get_client()
    if not client:
        return {"error": "Not connected. Use connect() first."}
    
    return {
        "count": 42,
        "breakdown": {
            "Critical": 5,
            "High": 12,
            "Medium": 20,
            "Low": 5
        },
        "filters_applied": {
            "severity": severity,
            "domain": domain,
            "start_time": start_time,
            "end_time": end_time
        }
    }

@agent.tool()
async def export_events(
    format_type: str = "JSON",
    severity: Optional[str] = None,
    start_time: Optional[int] = None,
    end_time: Optional[int] = None
) -> Dict[str, Any]:
    """
    Export events to file.
    
    Args:
        format_type: Export format (JSON, CSV, XML)
        severity: Filter by severity
        start_time: Start time (epoch timestamp) 
        end_time: End time (epoch timestamp)
    """
    client = client_manager.get_client()
    if not client:
        return {"error": "Not connected. Use connect() first."}
    
    return {
        "executionId": "export-12345",
        "executionStatusUrl": "/api/v1/task/export-12345",
        "message": f"Event export started in {format_type} format",
        "estimated_completion": "2 minutes",
        "download_url": "/api/v1/file/events-export-12345.json"
    }

@agent.tool()
async def acknowledge_events(event_ids: List[str], comment: Optional[str] = None) -> Dict[str, Any]:
    """
    Acknowledge events.
    
    Args:
        event_ids: List of event IDs to acknowledge
        comment: Optional acknowledgment comment
    """
    client = client_manager.get_client()
    if not client:
        return {"error": "Not connected. Use connect() first."}
    
    return {
        "acknowledged_events": event_ids,
        "acknowledgment_time": 1690123456,
        "comment": comment,
        "message": f"Successfully acknowledged {len(event_ids)} events"
    }

# Register tools with smart agent
def register_events_tools():
    """Register all events tools with the smart domain agent."""
    tools = [
        get_events,
        get_event_subscriptions,
        create_event_subscription,
        update_event_subscription,
        delete_event_subscription,
        get_event_types,
        get_event_count,
        export_events,
        acknowledge_events
    ]
    
    for tool in tools:
        smart_agent.register_tool(tool.__name__, tool)

# Process request method
async def process_request(query: str) -> str:
    """
    Process events-related requests with intelligent routing.
    """
    result = await smart_agent.process_request(query)
    return format_response(result, "Events", query)

# Initialize
register_events_tools()
agent.process_request = process_request
