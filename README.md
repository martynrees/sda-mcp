# Cisco Catalyst Center MCP Server

A comprehensive MCP server for Cisco Catalyst Center, providing access to the full suite of Catalyst Center Intent APIs—including, but not limited to, SDA (Software-Defined Access), Assurance, Site Management, Device Management, and more.

---

**Credit:** This project is inspired by the initial work of [Martyn Rees](https://github.com/martynrees/sda-mcp) (Author: Martyn Rees).

---

## Overview

This MCP server is designed for testing, learning, and automation with Cisco Catalyst Center APIs. It is not intended for production use. Use it in lab or development environments only.

## Features

- Access most Catalyst Center Intent APIs (SDA, Assurance, Sites, Devices, etc.)
- Easily extensible for new API endpoints
- Integrates with VS Code and GitHub Copilot Chat via MCP protocol
- Cross-platform support (Windows, macOS, Linux)

## Demo Video

🎥 [View Demo Video](https://app.vidcast.io/share/74a44822-0eaa-473d-8ea5-586572180013?playerMode=vidcast)

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

2. Clone the repository and navigate to the project directory:
   ```bash
   git clone <repository-url>
   cd cc-mcp
   ```

3. Install dependencies:
   ```bash
   uv sync
   ```

4. Run the MCP server:
   ```bash
   uv run python main.py
   ```

**Note:** The server will start and wait for MCP client connections via stdio. This is normal for MCP servers.

### Alternative Installation Methods

- **Using pip:**
  ```bash
  pip install -r requirements.txt
  python main.py
  ```
- **Using the setup script:**
  ```bash
  chmod +x setup.sh
  ./setup.sh
  ```
- **Using make:**
  ```bash
  make install  # Install dependencies
  make run      # Run the server
  ```

## VS Code Integration

To use this MCP server with VS Code and GitHub Copilot, follow these steps:

### 1. Configure VS Code Settings

1. Open VS Code settings (JSON format):
   - Press `Cmd+Shift+P` (macOS) or `Ctrl+Shift+P` (Windows/Linux)
   - Type "Preferences: Open User Settings (JSON)"
   - Select the option to open settings.json

2. Add or update the `mcpServers` configuration. Example configurations:

**Windows Example:**
```json
{
  "mcpServers": {
    "cc-mcp": {
      "type": "stdio",
      "command": "D:\\Workspace\\Ext_APIs\\CatC315\\cc-mcp\\.venv\\Scripts\\python.exe",
      "args": ["D:\\Workspace\\Ext_APIs\\CatC315\\cc-mcp\\main.py"]
    }
  }
}
```

**macOS/Linux Example:**
```json
{
  "mcpServers": {
    "cc-mcp": {
      "type": "stdio",
      "command": "/Users/username/Documents/cc-mcp/.venv/bin/python",
      "args": ["/Users/username/Documents/cc-mcp/main.py"],
      "cwd": "/Users/username/Documents/cc-mcp"
    }
  }
}
```

**Note:** Adjust the paths to match your project and virtual environment locations. On Windows, the `cwd` field is not required.

### 2. Start the MCP Server in VS Code

1. **Restart VS Code** after adding the configuration to ensure the MCP server settings are loaded.

2. **Connect to Catalyst Center** using GitHub Copilot:
   - Open GitHub Copilot Chat in VS Code
   - Use the `@cc-mcp` mention to access Catalyst Center tools
   - First, connect to your Catalyst Center instance:
     ```
     @cc-mcp connect to https://your-catalyst-center-ip username password
     ```

3. **Verify Connection:**
   - Test the connection and available tools:
     ```
     @cc-mcp what tools are available?
     ```
   - Or get network devices:
     ```
     @cc-mcp get network devices
     ```

### 3. Using the MCP Tools

Once connected, you can use various Catalyst Center tools through GitHub Copilot Chat:

- **Get fabric sites:** `@cc-mcp get fabric sites`
- **Get network devices:** `@cc-mcp get network devices`
- **Get virtual networks:** `@cc-mcp get layer 3 virtual networks`
- **Add fabric site:** `@cc-mcp add fabric site with site ID xyz`
- **Get assurance health:** `@cc-mcp get assurance health`
- **Get site hierarchy:** `@cc-mcp get site hierarchy`
- **And many more Catalyst Center operations...`

The MCP server will automatically start when VS Code loads and will be available through the `@cc-mcp` mention in GitHub Copilot Chat.

---

**Credit:** Initial idea and inspiration from [Martyn Rees](https://github.com/martynrees/sda-mcp) (Author: Martyn Rees).

