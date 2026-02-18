# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is an MCP (Model Context Protocol) implementation in Python demonstrating client-server communication with real-world data integration. The server provides tools to search and filter technical conferences from the [developers-conferences-agenda](https://github.com/scraly/developers-conferences-agenda) repository.

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
- Uses `FastMCP` from the `mcp.server.fastmcp` package for quick server setup
- Tools are defined using the `@mcp.tool()` decorator on simple Python functions
- Function parameters automatically define the tool's input schema
- Function docstrings become tool descriptions
- Runs as an HTTP server using `mcp.run(transport="streamable-http")`
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
1. Define a function with type hints for parameters
2. Add the `@mcp.tool()` decorator
3. Return a string or structured data
4. The function name becomes the tool name
5. Type hints define the input schema automatically
6. For async operations (like HTTP requests), use `async def`

Example:
```python
@mcp.tool()
def multiply(x: int, y: int) -> str:
    """Multiplies two numbers together."""
    return f"The product of {x} and {y} is {x * y}."
```

For async tools with external data:
```python
@mcp.tool()
async def fetch_data(query: str) -> str:
    """Fetch data from an external API."""
    async with httpx.AsyncClient() as client:
        response = await client.get(f"https://api.example.com/{query}")
        return response.text
```

## Data Sources

### Conference Data
The server reads conference data **locally** from the [developers-conferences-agenda](https://github.com/scraly/developers-conferences-agenda) repository, which is included as a git submodule in `data/developers-conferences-agenda/`.

**Data Source**: The server parses the `README.md` file in the submodule using a custom markdown parser (`mcp_server/markdown_parser.py`) that extracts:
- Conference names, dates, and locations
- CFP (Call for Papers) links and deadlines
- Event URLs and metadata

**Why Local Data?**
- No external API dependencies
- Faster response times (no network latency)
- Works offline
- Full control over data freshness

**Updating Conference Data**:
```bash
# Update the submodule to get the latest conferences
cd data/developers-conferences-agenda
git pull origin main
cd ../..
```

**Alternative**: The data is also available via public APIs if needed:
- Conferences: `https://developers.events/all-events.json`
- CFPs: `https://developers.events/all-cfps.json`

Conference data structure:
- `name`: Event name
- `date`: Array of timestamps (start and end)
- `city`, `country`, `location`: Geographic information
- `hyperlink`: Event website
- `cfp`: Object containing CFP link and deadline (`untilDate` is timestamp)
- `tags`: Array of topic tags

## Key Dependencies
- `mcp>=1.0.0`: Official MCP SDK providing FastMCP, ClientSession, and HTTP transports
  - Includes: httpx, httpx-sse, starlette, uvicorn, sse-starlette for HTTP transport
- `pytest-asyncio`: For testing async code

## Configuration Files
- `pyproject.toml`: Project metadata, dependencies, and tool configurations
- `mise.toml`: Environment variables for Anthropic API (used for testing/development)
- `.python-version`: Pins Python version for the project
