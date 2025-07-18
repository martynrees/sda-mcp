#!/bin/bash
# Setup script for uv-based development

set -e

echo "🚀 Setting up Catalyst Center MCP with uv..."

# Check if uv is installed
if ! command -v uv &> /dev/null; then
    echo "❌ uv is not installed. Installing now..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    echo "✅ uv installed successfully"
else
    echo "✅ uv is already installed ($(uv --version))"
fi

# Initialize uv project
echo "📦 Installing dependencies..."
uv sync

echo "🔧 Verifying installation..."
uv run python -c "import httpx, mcp; print('✅ Dependencies verified')"
uv run python -m py_compile main.py && echo "✅ Main module compiles successfully"

echo ""
echo "✅ Setup complete! You can now run:"
echo "   uv run python main.py        # Run the MCP server"
echo "   make run                      # Alternative way to run"
echo ""
echo "Development commands:"
echo "   make format                   # Format code with black and isort"
echo "   make lint                     # Lint code with ruff"
echo "   make type-check               # Type check with mypy"
echo "   make test                     # Run tests with pytest"
echo "   make help                     # Show all available commands"
