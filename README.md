# prez-mcp

Simple implementation of an MCP (Model Context Protocol) client and server in Python.

## Installation

This project uses `uv` for dependency management. Install dependencies:

```bash
uv sync --dev
uv pip install -e .
```

## Usage

### Running the client

The client connects to the server and demonstrates tool calls:

```bash
uv run python mcp_client/client.py
```

Or using the example script:

```bash
uv run python examples/run_client.py
```

### Running the server standalone

The server runs using stdio transport:

```bash
uv run python mcp_server/server.py
```

Or using the example script:

```bash
uv run python examples/run_server.py
```

## Available Tools

The server provides two simple tools:

- **echo**: Echoes back a provided message
- **add**: Adds two numbers together

## Testing

Run tests with pytest:

```bash
uv run pytest
```

## Code Quality

Format and lint code with ruff:

```bash
uv run ruff format .
uv run ruff check .
```

## Project Structure

- `mcp_server/` - MCP server implementation
- `mcp_client/` - MCP client implementation
- `examples/` - Example scripts for running client and server
- `tests/` - Test suite
