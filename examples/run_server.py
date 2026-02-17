#!/usr/bin/env -S uv run --script
"""Example: Run the MCP server directly."""

import asyncio
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from mcp_server.server import main

if __name__ == "__main__":
    print("Starting MCP Server...")
    print("The server will communicate via stdin/stdout (stdio protocol)")
    asyncio.run(main())
