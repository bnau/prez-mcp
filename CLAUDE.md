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
# Terminal 1: Start the HTTP server (listens on http://127.0.0.1:8000)
uv run python mcp_server/server.py

# Terminal 2: Run the client (connects to HTTP server)
uv run python mcp_client/client.py
```

**Note**: The server must be running before the client can connect. The server listens on `http://127.0.0.1:8000/mcp` by default.

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
- **Transport**: The MCP protocol uses HTTP with Streamable HTTP for communication between client and server
- **Protocol**: JSON-RPC based protocol for tool discovery and execution over HTTP POST/GET requests
- **Async**: Both client and server are fully asynchronous using asyncio
- **Streaming**: Supports SSE (Server-Sent Events) for real-time streaming responses

### Server (`mcp_server/server.py`)
- Creates an MCP Server instance with a name identifier
- Implements two decorators:
  - `@server.list_tools()`: Returns available tools and their schemas
  - `@server.call_tool()`: Handles tool execution based on name and arguments
- Runs as an HTTP server using Starlette (ASGI) and `StreamableHTTPSessionManager`
- Tools are defined with JSON schemas for input validation
- Listens on `http://127.0.0.1:8000/mcp` by default
- Supports stateful sessions (clients maintain session IDs across requests)

### Client (`mcp_client/client.py`)
- Connects to the HTTP server using `streamable_http_client(url)`
- Uses `AsyncExitStack` to manage multiple async context managers
- Session lifecycle:
  1. Connect to HTTP server URL
  2. Initialize ClientSession with read/write streams
  3. Call `session.initialize()`
  4. Use `session.list_tools()` and `session.call_tool()`
- Automatically handles HTTP requests and SSE streaming responses

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
- `mcp>=1.0.0`: Official MCP SDK providing Server, ClientSession, and HTTP transports
  - Includes: httpx, httpx-sse, starlette, uvicorn, sse-starlette for HTTP transport
- `pytest-asyncio`: For testing async code

## Configuration Files
- `pyproject.toml`: Project metadata, dependencies, and tool configurations
- `mise.toml`: Environment variables for Anthropic API (used for testing/development)
- `.python-version`: Pins Python version for the project
