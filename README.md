# Cisco Catalyst Center FastMCP Server

A comprehensive FastMCP server that provides access to most Cisco Catalyst Center Intent API endpoints for SDA (Software-Defined Access) operations.

## Overview

This MCP server is for testing and learning purposes only and should not be used in production. It is purely around the art of what is possible and should not be used for anything but lab purposes.



## Installation

### Using uv (Recommended)

1. Install uv if you haven't already:
```bash
# On macOS and Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# On Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# Or using pip
pip install uv
```

2. Install dependencies:
```bash
uv sync
```

3. Run the FastMCP server:
```bash
uv run python main.py
```

### Alternative Installation Methods

**Using pip (traditional):**
```bash
pip install -r requirements.txt
python main.py
```

