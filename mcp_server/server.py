"""Simple MCP Server implementation."""

import asyncio
import contextlib

from mcp.server import Server
from mcp.server.streamable_http_manager import StreamableHTTPSessionManager
from mcp.types import Tool
from starlette.applications import Starlette
from starlette.routing import Mount
import uvicorn

# Create server instance
server = Server("simple-mcp-server")


@server.list_tools()
async def list_tools() -> list[Tool]:
    """List available tools."""
    return [
        Tool(
            name="echo",
            description="Echo back the provided message",
            inputSchema={
                "type": "object",
                "properties": {
                    "message": {
                        "type": "string",
                        "description": "The message to echo back",
                    }
                },
                "required": ["message"],
            },
        ),
        Tool(
            name="add",
            description="Add two numbers together",
            inputSchema={
                "type": "object",
                "properties": {
                    "a": {"type": "number", "description": "First number"},
                    "b": {"type": "number", "description": "Second number"},
                },
                "required": ["a", "b"],
            },
        ),
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[dict]:
    """Handle tool calls."""
    if name == "echo":
        message = arguments["message"]
        return [{"type": "text", "text": f"Echo: {message}"}]

    elif name == "add":
        a = arguments["a"]
        b = arguments["b"]
        result = a + b
        return [{"type": "text", "text": f"Result: {result}"}]

    else:
        raise ValueError(f"Unknown tool: {name}")


async def main():
    """Run the MCP server over HTTP."""
    # Create session manager for handling HTTP transport
    manager = StreamableHTTPSessionManager(server, stateless=False)

    # Define lifespan to manage the session manager lifecycle
    @contextlib.asynccontextmanager
    async def lifespan(app):
        async with manager.run():
            yield

    # Create Starlette ASGI application
    app = Starlette(
        routes=[Mount("/mcp", app=manager.handle_request)],
        lifespan=lifespan,
    )

    # Run the server with uvicorn
    config = uvicorn.Config(
        app,
        host="127.0.0.1",
        port=8000,
        log_level="info",
    )
    server_instance = uvicorn.Server(config)
    await server_instance.serve()


if __name__ == "__main__":
    asyncio.run(main())
