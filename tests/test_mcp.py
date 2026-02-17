"""Test the MCP server and client."""

import pytest


@pytest.mark.asyncio
async def test_server_tools():
    """Test that server provides expected tools."""
    from mcp_server.server import list_tools

    tools = await list_tools()
    tool_names = [tool.name for tool in tools]

    assert "echo" in tool_names
    assert "add" in tool_names


@pytest.mark.asyncio
async def test_echo_tool():
    """Test the echo tool."""
    from mcp_server.server import call_tool

    result = await call_tool("echo", {"message": "test message"})

    assert len(result) == 1
    assert result[0]["type"] == "text"
    assert "Echo: test message" in result[0]["text"]


@pytest.mark.asyncio
async def test_add_tool():
    """Test the add tool."""
    from mcp_server.server import call_tool

    result = await call_tool("add", {"a": 10, "b": 5})

    assert len(result) == 1
    assert result[0]["type"] == "text"
    assert "Result: 15" in result[0]["text"]


@pytest.mark.asyncio
async def test_unknown_tool():
    """Test handling of unknown tool."""
    from mcp_server.server import call_tool

    with pytest.raises(ValueError, match="Unknown tool"):
        await call_tool("unknown_tool", {})
