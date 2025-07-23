from mcp_instance import mcp  # Import the shared instance
from sda import *
from task import *
from client import *


if __name__ == "__main__":
    import sys

    # Check if we should run as HTTP server (for testing/debugging)
    if len(sys.argv) > 1 and sys.argv[1] == "--http":
        import uvicorn

        # Run as HTTP server for testing
        uvicorn.run(mcp.app, host="0.0.0.0", port=8000)
    else:
        # Initialize and run the MCP server
        mcp.run(transport="stdio")
