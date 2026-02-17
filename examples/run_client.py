#!/usr/bin/env -S uv run --script
"""Example: Run the MCP client to interact with the server."""

import asyncio
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from mcp_client.client import main

if __name__ == "__main__":
    asyncio.run(main())
