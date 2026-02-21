"""Simple MCP Client implementation using FastMCP 3."""

import asyncio

from fastmcp.client import Client


async def run_client():
    """Run the MCP client to interact with the server."""
    # Server URL for HTTP transport
    url = "http://127.0.0.1:8000/mcp"

    # Create client that connects via HTTP
    client = Client(url)

    async with client:
        # List available tools
        tools_list = await client.list_tools()
        print("=" * 80)
        print("AVAILABLE TOOLS")
        print("=" * 80)
        for tool in tools_list:
            print(f"  - {tool.name}: {tool.description or 'No description'}")
        print()

        # List available resources
        resources_list = await client.list_resources()
        print("=" * 80)
        print("AVAILABLE RESOURCES")
        print("=" * 80)
        for resource in resources_list:
            print(f"  - {resource.uri}")
            print(f"    Name: {resource.name or 'N/A'}")
            print(f"    Description: {resource.description or 'N/A'}")
        print()

        # List available prompts
        prompts_list = await client.list_prompts()
        print("=" * 80)
        print("AVAILABLE PROMPTS")
        print("=" * 80)
        for prompt in prompts_list:
            print(f"  - {prompt.name}: {prompt.description or 'No description'}")
        print()

        # Read CFP resources
        print("=" * 80)
        print("TEST: Read CFP Resources")
        print("=" * 80)
        for resource_uri in ["cfp://mcp", "cfp://ide", "cfp://kagent"]:
            print(f"\n{resource_uri}:")
            print("-" * 80)
            resource_result = await client.read_resource(resource_uri)
            # resource_result is a list of content items
            for content in resource_result:
                # Display first 300 characters of the content
                text = content.text if hasattr(content, "text") else str(content)
                preview = text[:300] + "..." if len(text) > 300 else text
                print(preview)
            print()

        # Search conferences by date
        print("=" * 80)
        print("TEST: Search Conferences by Date (June 2026)")
        print("=" * 80)
        date_result = await client.call_tool(
            "search_conferences", {"min_date": "2026-06-01", "max_date": "2026-06-30"}
        )
        # date_result is a CallToolResult with a content attribute
        for content in date_result.content:
            text = content.text if hasattr(content, "text") else str(content)
            print(f"{text}")
        print()

        # Search conferences by city
        print("=" * 80)
        print("TEST: Search Conferences by Country (France)")
        print("=" * 80)
        city_result = await client.call_tool("search_conferences", {"country": "France"})
        for content in city_result.content:
            text = content.text if hasattr(content, "text") else str(content)
            print(f"{text}")
        print()

        # Test the prompt
        print("=" * 80)
        print("TEST: Use Prompt to List Conferences (June 2026, France)")
        print("=" * 80)
        prompt_result = await client.get_prompt(
            "list_conferences_by_month_and_country", {"month": "2026-06", "country": "France"}
        )
        print("Generated Prompt:")
        print("-" * 80)
        # prompt_result contains messages
        if hasattr(prompt_result, "messages"):
            for message in prompt_result.messages:
                role = message.role.upper() if hasattr(message, "role") else "UNKNOWN"
                if hasattr(message.content, "text"):
                    text = message.content.text
                else:
                    text = str(message.content)
                print(f"{role}: {text}")
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
