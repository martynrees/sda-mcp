# mcp_instance.py
# Shared FastMCP instance to be used across all modules

from mcp.server.fastmcp import FastMCP

def create_mcp_instance(name: str) -> FastMCP:
    """Creates and returns a new FastMCP instance."""
    return FastMCP(name)
