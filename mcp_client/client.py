"""Simple MCP Client implementation."""

import asyncio
from contextlib import AsyncExitStack

from mcp import ClientSession
from mcp.client.streamable_http import streamable_http_client


async def run_client():
    """Run the MCP client to interact with the server."""
    # Server URL for HTTP transport
    url = "http://127.0.0.1:8000/mcp"

    async with AsyncExitStack() as stack:
        # Connect to HTTP server
        read_stream, write_stream, get_session_id = await stack.enter_async_context(
            streamable_http_client(url)
        )
        session = await stack.enter_async_context(ClientSession(read_stream, write_stream))

        # Initialize session
        await session.initialize()

        # List available tools
        tools_list = await session.list_tools()
        print("=" * 80)
        print("AVAILABLE TOOLS")
        print("=" * 80)
        for tool in tools_list.tools:
            print(f"  - {tool.name}: {tool.description}")
        print()

        # Search conferences by date
        print("=" * 80)
        print("TEST: Search Conferences by Date (June 2026)")
        print("=" * 80)
        date_result = await session.call_tool(
            "search_conferences", {"min_date": "2026-06-01", "max_date": "2026-06-30"}
        )
        for content in date_result.content:
            print(f"{content.text}")
        print()

        # Search conferences by city
        print("=" * 80)
        print("TEST: Search Conferences by Country (France)")
        print("=" * 80)
        city_result = await session.call_tool("search_conferences", {"country": "France"})
        for content in city_result.content:
            print(f"{content.text}")
        print()

async def main():
    """Main entry point."""
    try:
        await run_client()
    except Exception as e:
        print(f"Error: {e}")
        raise


if __name__ == "__main__":
    asyncio.run(main())
