# mcp_instance.py
# Shared FastMCP instance to be used across all modules

from mcp.server.fastmcp import FastMCP

# Single global MCP instance
mcp = FastMCP("CatC-MCP")
