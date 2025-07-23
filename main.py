from agents.router import router_agent
from client import *


if __name__ == "__main__":
    import sys

    # Check if we should run as HTTP server (for testing/debugging)
    if len(sys.argv) > 1 and sys.argv[1] == "--http":
        import uvicorn

        # Run as HTTP server for testing
        uvicorn.run(router_agent.app, host="0.0.0.0", port=8000)
    else:
        # Initialize and run the MCP server
        router_agent.run(transport="stdio")
