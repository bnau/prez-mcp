# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a simple MCP (Model Context Protocol) implementation in Python demonstrating client-server communication. The codebase is intentionally kept minimal and straightforward.

## Development Commands

This project uses `uv` for dependency management.

### Setup
```bash
uv sync --dev  # Install all dependencies including dev dependencies
uv pip install -e .  # Install package in editable mode (needed for tests)
```

### Running
```bash
# Run the client (connects to server and demonstrates tool calls)
uv run python mcp_client/client.py

# Run the server (stdio-based, meant to be called by client)
uv run python mcp_server/server.py

# Using example scripts
uv run python examples/run_client.py
uv run python examples/run_server.py
```

### Testing
```bash
# Run all tests
uv run pytest

# Run specific test file
uv run pytest tests/test_mcp.py

# Run with verbose output
uv run pytest -v

# Run specific test
uv run pytest tests/test_mcp.py::test_echo_tool
```

### Code Quality
```bash
# Format code
uv run ruff format .

# Lint code
uv run ruff check .

# Auto-fix linting issues
uv run ruff check --fix .
```

## Architecture

### Communication Pattern
- **Transport**: The MCP protocol uses stdio (standard input/output) for communication between client and server
- **Protocol**: JSON-RPC based protocol for tool discovery and execution
- **Async**: Both client and server are fully asynchronous using asyncio

### Server (`mcp_server/server.py`)
- Creates an MCP Server instance with a name identifier
- Implements two decorators:
  - `@server.list_tools()`: Returns available tools and their schemas
  - `@server.call_tool()`: Handles tool execution based on name and arguments
- Runs using `stdio_server()` context manager for stdio transport
- Tools are defined with JSON schemas for input validation

### Client (`mcp_client/client.py`)
- Connects to the server using `StdioServerParameters` (command + args)
- Uses `AsyncExitStack` to manage multiple async context managers
- Session lifecycle:
  1. Create stdio transport
  2. Initialize ClientSession
  3. Call `session.initialize()`
  4. Use `session.list_tools()` and `session.call_tool()`

### Adding New Tools
To add a new tool to the server:
1. Add tool definition in `list_tools()` with name, description, and inputSchema
2. Add tool handler in `call_tool()` matching the tool name
3. Return list of content dictionaries with `type` and `text` fields

### Tool Response Format
Tools must return a list of content dictionaries:
```python
[{"type": "text", "text": "Your response here"}]
```

## Key Dependencies
- `mcp>=1.0.0`: Official MCP SDK providing Server, ClientSession, and stdio transport
- `pytest-asyncio`: For testing async code

## Configuration Files
- `pyproject.toml`: Project metadata, dependencies, and tool configurations
- `mise.toml`: Environment variables for Anthropic API (used for testing/development)
- `.python-version`: Pins Python version for the project
