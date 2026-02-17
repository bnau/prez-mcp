"""Simple MCP Client implementation."""

import asyncio
from contextlib import AsyncExitStack

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def run_client():
    """Run the MCP client to interact with the server."""
    server_params = StdioServerParameters(
        command="python",
        args=["mcp_server/server.py"],
    )

    async with AsyncExitStack() as stack:
        # Connect to server
        stdio_transport = await stack.enter_async_context(stdio_client(server_params))
        stdio, write = stdio_transport
        session = await stack.enter_async_context(ClientSession(stdio, write))

        # Initialize session
        await session.initialize()

        # List available tools
        tools_list = await session.list_tools()
        print("Available tools:")
        for tool in tools_list.tools:
            print(f"  - {tool.name}: {tool.description}")
        print()

        # Call echo tool
        echo_result = await session.call_tool("echo", {"message": "Hello, MCP!"})
        print("Echo tool result:")
        for content in echo_result.content:
            print(f"  {content.text}")
        print()

        # Call add tool
        add_result = await session.call_tool("add", {"a": 42, "b": 8})
        print("Add tool result:")
        for content in add_result.content:
            print(f"  {content.text}")


async def main():
    """Main entry point."""
    try:
        await run_client()
    except Exception as e:
        print(f"Error: {e}")
        raise


if __name__ == "__main__":
    asyncio.run(main())
