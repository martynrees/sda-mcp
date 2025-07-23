from typing import Any, Dict, Optional

from mcp_instance import create_mcp_instance

agent = create_mcp_instance("TaskAgent")
from client import client_manager

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
    if "response" in response:
        resp = response["response"]

        # Check for taskId field
        if "taskId" in resp:
            return resp["taskId"]

        # Check for url field with task ID
        if "url" in resp:
            url = resp["url"]
            # Extract task ID from URL like "/api/v1/task/12345-..."
            if "/task/" in url:
                return url.split("/task/")[-1]

    # Check for taskId at top level
    if "taskId" in response:
        return response["taskId"]

    # Check for executionId (some APIs use this)
    if "executionId" in response:
        return response["executionId"]

    return None


@agent.tool()
async def execute_and_monitor_task(
    operation_name: str, operation_func, *args, auto_wait: bool = True, max_wait_seconds: int = 300, **kwargs
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
    client = client_manager.get_client()
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


@agent.tool()
async def get_task_by_id(task_id: str) -> Optional[Dict[str, Any]]:
    """Get task details by task ID

    Retrieves the details of a specific task using its task ID. This is useful for checking
    the status of operations that return a task ID (like most POST operations).

    Args:
        task_id: The unique identifier for the task
    """
    client = client_manager.get_client()
    if not client:
        return {"error": "Not connected. Use connect() first."}

    kwargs = {}
    return await client.request("GET", f"/dna/intent/api/v1/task/{task_id}", **kwargs)


@agent.tool()
async def get_tasks(
    offset: Optional[int] = None,
    limit: Optional[int] = None,
    status: Optional[str] = None,
    parent_id: Optional[str] = None,
    root_id: Optional[str] = None,
    start_time: Optional[int] = None,
    end_time: Optional[int] = None,
    sort_by: Optional[str] = None,
    order: Optional[str] = None,
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
    client = client_manager.get_client()
    if not client:
        return {"error": "Not connected. Use connect() first."}

    params = {}
    if offset is not None:
        params["offset"] = offset
    if limit is not None:
        params["limit"] = limit
    if status is not None:
        params["status"] = status
    if parent_id is not None:
        params["parentId"] = parent_id
    if root_id is not None:
        params["rootId"] = root_id
    if start_time is not None:
        params["startTime"] = start_time
    if end_time is not None:
        params["endTime"] = end_time
    if sort_by is not None:
        params["sortBy"] = sort_by
    if order is not None:
        params["order"] = order

    kwargs = {}
    if params:
        kwargs["params"] = params

    return await client.request("GET", f"/dna/intent/api/v1/tasks", **kwargs)


@agent.tool()
async def check_task_status(task_id: str) -> str:
    """Check the status of a task and return a human-readable summary

    This is a convenience function that gets task details and returns a formatted
    status summary including success/failure state, progress, and any error messages.

    Args:
        task_id: The unique identifier for the task
    """
    client = client_manager.get_client()
    if not client:
        return "Error: Not connected. Use connect() first."

    task_response = await get_task_by_id(task_id)

    if not task_response or "response" not in task_response:
        return f"Error: Could not retrieve task {task_id}"

    task = task_response["response"]

    # Extract key information
    task_id_actual = task.get("id", "Unknown")
    is_error = task.get("isError", False)
    progress = task.get("progress", "Unknown")
    start_time = task.get("startTime", 0)
    end_time = task.get("endTime", 0)
    failure_reason = task.get("failureReason", "")
    error_code = task.get("errorCode", "")
    service_type = task.get("serviceType", "Unknown")

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
        summary += """
                    Error Details:
                    --------------
                    """
        if error_code:
            summary += f"\nError Code: {error_code}"
        if failure_reason:
            summary += f"\nFailure Reason: {failure_reason}"

    return summary.strip()


@agent.tool()
async def wait_for_task_completion(task_id: str, max_wait_seconds: int = 300, check_interval_seconds: int = 5) -> str:
    """Wait for a task to complete and return the final status

    Polls a task until it completes (success or failure) or until the maximum wait time is reached.

    Args:
        task_id: The unique identifier for the task
        max_wait_seconds: Maximum time to wait for completion (default: 300 seconds)
        check_interval_seconds: How often to check the task status (default: 5 seconds)
    """
    import asyncio
    import time

    client = client_manager.get_client()
    if not client:
        return "Error: Not connected. Use connect() first."

    start_wait_time = time.time()
    max_wait_time = start_wait_time + max_wait_seconds

    while time.time() < max_wait_time:
        task_response = await get_task_by_id(task_id)

        if not task_response or "response" not in task_response:
            return f"Error: Could not retrieve task {task_id}"

        task = task_response["response"]
        is_error = task.get("isError", False)
        end_time = task.get("endTime", 0)

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


@agent.tool()
async def get_recent_failed_tasks(limit: int = 10) -> str:
    """Get recent failed tasks for troubleshooting

    Retrieves the most recent failed tasks to help with troubleshooting operations.

    Args:
        limit: Maximum number of failed tasks to return (default: 10)
    """
    client = client_manager.get_client()
    if not client:
        return "Error: Not connected. Use connect() first."

    # Get recent failed tasks
    tasks_response = await get_tasks(status="FAILURE", limit=limit, sort_by="startTime", order="desc")

    if not tasks_response or "response" not in tasks_response:
        return "No failed tasks found or error retrieving tasks."

    tasks = tasks_response["response"]

    if not tasks:
        return "No recent failed tasks found."

    formatted_tasks = []
    for task in tasks:
        task_id = task.get("id", "Unknown")
        service_type = task.get("serviceType", "Unknown")
        failure_reason = task.get("failureReason", "Unknown reason")
        error_code = task.get("errorCode", "")
        start_time = task.get("startTime", 0)

        # Convert timestamp to readable format
        import datetime

        if start_time > 0:
            dt = datetime.datetime.fromtimestamp(start_time / 1000)
            time_str = dt.strftime("%Y-%m-%d %H:%M:%S")
        else:
            time_str = "Unknown"

        formatted = f"""
                    Task ID: {task_id}
                    Service: {service_type}
                    Time: {time_str}
                    Error Code: {error_code}
                    Reason: {failure_reason}
                    """
        formatted_tasks.append(formatted.strip())

    return "Recent Failed Tasks:\n" + "\n---\n".join(formatted_tasks)
