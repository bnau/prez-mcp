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

        # List available resources
        resources_list = await session.list_resources()
        print("=" * 80)
        print("AVAILABLE RESOURCES")
        print("=" * 80)
        for resource in resources_list.resources:
            print(f"  - {resource.uri}")
            print(f"    Name: {resource.name}")
            print(f"    Description: {resource.description}")
        print()

        # List available prompts
        prompts_list = await session.list_prompts()
        print("=" * 80)
        print("AVAILABLE PROMPTS")
        print("=" * 80)
        for prompt in prompts_list.prompts:
            print(f"  - {prompt.name}: {prompt.description}")
        print()

        # Read CFP resources
        print("=" * 80)
        print("TEST: Read CFP Resources")
        print("=" * 80)
        for resource_uri in ["cfp://mcp", "cfp://ide", "cfp://kagent"]:
            print(f"\n{resource_uri}:")
            print("-" * 80)
            resource_result = await session.read_resource(resource_uri)
            for content in resource_result.contents:
                # Display first 300 characters of the content
                text = content.text
                preview = text[:300] + "..." if len(text) > 300 else text
                print(preview)
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

        # Test the prompt
        print("=" * 80)
        print("TEST: Use Prompt to List Conferences (June 2026, France)")
        print("=" * 80)
        prompt_result = await session.get_prompt(
            "list_conferences_by_month_country", {"month": "2026-06", "country": "France"}
        )
        print("Generated Prompt:")
        print("-" * 80)
        for message in prompt_result.messages:
            print(f"{message.role.upper()}: {message.content.text}")
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
