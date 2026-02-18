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

### Running the server standalone

The server runs using stdio transport:

```bash
uv run python mcp_server/server.py
```

## Available Tools

The server provides 3 tools:

### Conference Tools
- **search_conferences_by_date**: Search for tech conferences within a date range
  - Parameters: `start_date` (YYYY-MM-DD), `end_date` (optional, YYYY-MM-DD)
  - Returns: List of conferences happening in the specified period

- **search_conferences_by_city**: Search for conferences in a specific city
  - Parameters: `city` (string, case-insensitive)
  - Returns: List of conferences in the matching city

- **search_conferences_by_cfp**: Search for conferences with open Call for Papers
  - Parameters: `start_date` (optional, YYYY-MM-DD), `end_date` (optional, YYYY-MM-DD)
  - Returns: List of conferences with CFPs, optionally filtered by deadline date

Conference data is sourced from [developers-conferences-agenda](https://github.com/scraly/developers-conferences-agenda) via the [developers.events](https://developers.events) API.

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
- `tests/` - Test suite
