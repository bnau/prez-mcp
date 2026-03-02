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
- **Library**: Uses FastMCP 3 - a standalone, simplified MCP implementation

### Server (`mcp_server/server.py`)
- Uses `FastMCP` from the `fastmcp` package (FastMCP 3)
- Tools are defined using the `@mcp.tool()` decorator on simple Python functions
- Function parameters automatically define the tool's input schema
- Function docstrings become tool descriptions
- Runs as an HTTP server using `mcp.run(transport="streamable-http")`
- Listens on `http://127.0.0.1:8000/mcp` by default
- Supports stateful sessions (clients maintain session IDs across requests)

### Client (`mcp_client/client.py`)
- Uses `Client` from `fastmcp.client` (FastMCP 3)
- Simple connection pattern: `Client(url)` where url is the server HTTP endpoint
- Supports async context manager: `async with client:`
- Direct method calls:
  - `await client.list_tools()` - Get available tools
  - `await client.call_tool(name, args)` - Execute a tool
  - `await client.list_resources()` - Get available resources
  - `await client.read_resource(uri)` - Read a resource
  - `await client.list_prompts()` - Get available prompts
  - `await client.get_prompt(name, args)` - Get a prompt

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

**Using Context for advanced features:**
Tools can accept a `Context` parameter to access sampling (AI) and elicitation (user input):
```python
from fastmcp.server.context import Context

@mcp.tool()
async def advanced_tool(
    ctx: Context,  # Must be first parameter
    query: str,
) -> str:
    """Tool with AI sampling and user confirmation."""
    # Use AI to analyze data
    result = await ctx.sample(
        messages="Analyze this query: " + query,
        temperature=0.3,
        max_tokens=1000,
    )

    # Ask user for confirmation
    confirmation = await ctx.elicit(
        "Do you want to proceed?",
        response_type=bool
    )

    if confirmation.action == "accept" and confirmation.data:
        return f"Proceeding with: {result.text}"
    return "Operation cancelled"
```

### Adding Resources
Resources expose read-only data through URI patterns:

**Dynamic resources with URI templates:**
```python
@mcp.resource(
    uri="cfp://{theme}",
    name="CFP Content by Theme",
    description="Read CFP content for a given theme",
    mime_type="text/markdown",
)
def get_cfp(theme: str) -> str:
    cfp_file = CFP_SUBJECTS_DIR / f"{theme}.md"
    if cfp_file.exists():
        return cfp_file.read_text(encoding="utf-8")
    return "CFP not found"
```

**Static file resources:**
```python
from fastmcp.resources import FileResource

resource = FileResource(
    uri="file:///path/to/file.md",
    path=Path("/path/to/file.md"),
    name="file_name",
    mime_type="text/markdown",
)
mcp.add_resource(resource)
```

### Adding Prompts
Prompts are reusable templates that return instructions for common tasks:

```python
@mcp.prompt(
    name="list_conferences_by_month_and_country",
    description="Generate a prompt to list all technical conferences in a specific month and country",
)
def list_conferences_by_month_country(
    month: Annotated[str, Field(description="Month in YYYY-MM format")],
    country: Annotated[str, Field(description="Country name")],
) -> str:
    """Generate a prompt to search conferences by month and country."""
    # Calculate date range
    year, month_num = month.split("-")
    # Return formatted prompt text
    return f"Please search for conferences in {country} during {month}..."
```

Prompts can include:
- Instructions for calling tools
- Formatting guidelines for output
- Suggestions for handling edge cases

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
- `fastmcp>=3.0.0`: FastMCP 3 - standalone MCP implementation providing FastMCP server and Client
  - Includes: httpx, uvicorn, starlette for HTTP transport
- `pytest-asyncio`: For testing async code

## Advanced Features

### AI-Powered CFP Matching (Sampling)
The server supports AI-powered matching between CFP proposals and conferences using `ctx.sample()`:
- The `search_conferences` tool has a `match_cfps` parameter that triggers AI analysis
- When enabled, the server reads all CFP files from `mcp_server/sujets_cfp/*.md`
- For each CFP, it uses LLM sampling to analyze which conferences are relevant
- Returns match scores (0-100) and reasoning for each conference

**Parameters for CFP matching:**
- `match_cfps=True`: Enable AI matching
- `min_score`: Minimum match score threshold (default: 30)
- `cfp_open=True`: Only show conferences with open CFPs

**Client-side sampling handlers:**
The client must provide a sampling handler to process `ctx.sample()` requests from the server:
```python
from fastmcp.client import Client

async def sampling_handler(messages, params, context):
    # Call your LLM and return the response
    return llm_response_json

client = Client(url, sampling_handler=sampling_handler)
```

See `mcp_client/client.py` for a complete example with user confirmation prompts and LLM integration.

### User Confirmations (Elicitation)
The server can request user confirmations using `ctx.elicit()`:
- Used for interactive decisions (e.g., "Do you want to submit this CFP?")
- Returns `ElicitResult` with action ("accept", "decline", "cancel") and data
- The client must provide an elicitation handler

**Client-side elicitation handler:**
```python
async def elicitation_handler(prompt, response_type, params, context):
    # Ask user for confirmation
    answer = input(prompt)
    return ElicitResult(action="accept", content=True)

client = Client(url, elicitation_handler=elicitation_handler)
```

### Intelligent Client Pattern (Prompt → LLM → Tool Call)
The client demonstrates an advanced pattern:
1. **Get Prompt**: Retrieve a pre-configured prompt from the server
2. **LLM Analysis**: Send prompt + available tools to an LLM
3. **Tool Execution**: LLM decides which MCP tools to call
4. **Result Processing**: LLM formats the final response

This pattern is implemented in the `LLMOrchestrator` class in `mcp_client/client.py`.

### Testing Patterns
Tests use pytest with async support and mocking:
- Use `@pytest.fixture` for reusable test data (e.g., mock conferences)
- Mock `parser_service.get_conferences()` to avoid reading actual files
- Test files are in `tests/` directory and follow the pattern `test_*.py`
- Run specific test classes: `uv run pytest tests/test_server.py::TestSearchConferences`
- Run specific test methods: `uv run pytest tests/test_server.py::TestSearchConferences::test_search_by_country`

## Configuration Files
- `pyproject.toml`: Project metadata, dependencies, and tool configurations
- `mise.toml`: Environment variables for Anthropic API (used for testing/development)
- `.python-version`: Pins Python version for the project

## Important Implementation Details

### CFP Subjects Directory
- Location: `mcp_server/sujets_cfp/`
- Contains markdown files (`.md`) for CFP proposals
- Each file becomes a resource accessible via `cfp://{theme}` URI
- Files are also exposed as file resources via `file://` URIs
- Used by the `match_cfps` feature for AI-powered matching

### Markdown Parser Service
- Location: `mcp_server/markdown_parser.py`
- Parses conference data from `data/developers-conferences-agenda/README.md`
- Converts markdown tables into structured conference dictionaries
- Handles date parsing, CFP extraction, and tag normalization
