# Cisco Catalyst Center FastMCP Server

A comprehensive FastMCP server that provides access to most Cisco Catalyst Center Intent API endpoints for SDA (Software-Defined Access) operations.

## Overview

This MCP server is for testing and learning purposes only and should not be used in production. It is purely around the art of what is possible and should not be used for anything but lab purposes.

### Demo Video

Watch a demonstration of the MCP server in action:

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
cd SDA-MCP
```

3. Install dependencies:
```bash
uv sync
```

4. Run the FastMCP server:
```bash
uv run python main.py
```

**Note:** The server will start and wait for MCP client connections via stdio. This is normal behavior for MCP servers.

### Alternative Installation Methods

**Using pip (traditional):**
```bash
pip install -r requirements.txt
python main.py
```

**Using the setup script:**
```bash
chmod +x setup.sh
./setup.sh
```

**Using make (if you have make installed):**
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

2. Add or update the `mcpServers` configuration:

```json
{
  "mcpServers": {
    "sda": {
      "command": "/path/to/your/project/.venv/bin/python",
      "args": ["/path/to/your/project/main.py"],
      "cwd": "/path/to/your/project"
    }
  }
}
```

**Example paths:**
- **command**: `/Users/username/Documents/SDA-MCP/.venv/bin/python`
- **args**: `["/Users/username/Documents/SDA-MCP/main.py"]`
- **cwd**: `/Users/username/Documents/SDA-MCP`

**Note:** Replace `/path/to/your/project` with the actual path to your SDA-MCP project directory, and ensure the virtual environment path matches your setup.

### 2. Start the MCP Server in VS Code

1. **Restart VS Code** after adding the configuration to ensure the MCP server settings are loaded

2. **Connect to Catalyst Center** using GitHub Copilot:
   - Open GitHub Copilot Chat in VS Code
   - Use the `@sda` mention to access SDA-specific tools
   - First, connect to your Catalyst Center instance:
     ```
     @sda connect to https://your-catalyst-center-ip username password
     ```

3. **Verify Connection**:
   - You can test the connection and available tools by asking:
     ```
     @sda what tools are available?
     ```
   - Or get network devices:
     ```
     @sda get network devices
     ```

### 3. Using the MCP Tools

Once connected, you can use various SDA tools through GitHub Copilot Chat:

- **Get fabric sites**: `@sda get fabric sites`
- **Get network devices**: `@sda get network devices`
- **Get virtual networks**: `@sda get layer 3 virtual networks`
- **Add fabric site**: `@sda add fabric site with site ID xyz`
- **And many more SDA operations...**

The MCP server will automatically start when VS Code loads and will be available through the `@sda` mention in GitHub Copilot Chat.

