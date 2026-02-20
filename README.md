# prez-mcp

Simple implementation of an MCP (Model Context Protocol) client and server in Python.

## Features

- **FastMCP Server**: Easy-to-use MCP server using the `@mcp.tool()`, `@mcp.resource()`, and `@mcp.prompt()` decorators
- **Conference Search Tool**: Search and filter technical conferences by date, country, and tags
- **MCP Prompts**: Pre-configured prompts to help users discover conferences by month and country
- **CFP Resources**: Access three CFP (Call for Papers) proposals through MCP resources:
  - `cfp://mcp` - MCP in practice talk
  - `cfp://ide` - AI-powered code assistants comparison
  - `cfp://kagent` - KAgent + KServe for AI agent industrialization
- **Real Data**: Parses conference data from the [developers-conferences-agenda](https://github.com/scraly/developers-conferences-agenda) repository

## Installation

This project uses `uv` for dependency management. Install dependencies:

```bash
uv sync --dev
uv pip install -e .
```

## Usage

### Running the server

The server runs using HTTP transport on `http://127.0.0.1:8000/mcp`:

```bash
uv run python mcp_server/server.py
```

### Running the client

The client connects to the server and demonstrates tool calls and resource access:

```bash
uv run python mcp_client/client.py
```

## Available Tools

The server provides one main tool:

### search_conferences
Search for technical conferences with optional filters:
- **Parameters**:
  - `min_date` (optional): Minimum conference date (YYYY-MM-DD format)
  - `max_date` (optional): Maximum conference date (YYYY-MM-DD format)
  - `country` (optional): Country name to filter by (case-insensitive partial match)
  - `tags` (optional): Comma-separated list of tags to filter by (e.g., 'python,ai,web')
- **Returns**: List of conferences with metadata (dates, location, CFP deadlines, tags, etc.)

**Example usage:**
```python
# Search conferences in France happening in June 2026
search_conferences(min_date='2026-06-01', max_date='2026-06-30', country='France')

# Search AI conferences
search_conferences(tags='ai,machine-learning')
```

## Available Prompts

The server provides ready-to-use prompts to simplify common tasks:

### list_conferences_by_month_country
Generate a prompt to list all technical conferences in a specific month and country.

- **Parameters**:
  - `month`: Month in YYYY-MM format (e.g., '2026-06' for June 2026)
  - `country`: Country name (e.g., 'France', 'USA', 'Germany')
- **Returns**: A formatted prompt that instructs how to search for conferences and format the results

**Example usage:**
```python
# Get a prompt to list conferences in France during June 2026
prompt_result = await session.get_prompt(
    "list_conferences_by_month_country",
    {"month": "2026-06", "country": "France"}
)
```

The prompt will automatically:
- Calculate the first and last day of the specified month
- Generate appropriate date range parameters
- Provide formatting instructions for a clear table output
- Suggest alternatives if no conferences are found

## Available Resources

The server exposes three CFP proposals as MCP resources:

### cfp://mcp
**MCP in practice: an application to understand everything**

Model Context Protocol talk covering architecture, lifecycle, server/client development, and production integration.

### cfp://ide
**Copilot, Cursor & co: Exploring AI-powered code assistants**

A comprehensive comparison of AI coding assistants (Copilot, Cursor, Claude Code, etc.) with concrete evaluation criteria, demos, and practical guidance for choosing the right tool.

### cfp://kagent
**KAgent + KServe: The perfect combo for industrializing AI agents**

Learn how to deploy and scale AI agents using KAgent and KServe on Kubernetes with a cloud-native approach, using MCP and A2A protocols.

**Accessing resources:**
```python
# Read a CFP resource
session.read_resource("cfp://mcp")
```

Conference data is sourced from [developers-conferences-agenda](https://github.com/scraly/developers-conferences-agenda) via local parsing.

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
