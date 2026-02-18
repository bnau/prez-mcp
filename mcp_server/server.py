"""Simple MCP Server implementation."""

from datetime import datetime
from typing import Optional

from mcp.server.fastmcp import FastMCP

try:
    from .markdown_parser import MarkdownParserService
except ImportError:
    # When running as script directly
    from markdown_parser import MarkdownParserService

# Create server instance
mcp = FastMCP("cfp-server")

# Initialize the markdown parser service
parser_service = MarkdownParserService()


@mcp.tool()
def search_conferences(
    min_date: Optional[str] = None,
    max_date: Optional[str] = None,
    country: Optional[str] = None,
) -> str:
    """
    Search for conferences with optional filters.

    Args:
        min_date: Optional minimum conference date in format YYYY-MM-DD
        max_date: Optional maximum conference date in format YYYY-MM-DD
        country: Optional country name to filter by (case-insensitive partial match)

    Returns:
        List of matching conferences
    """
    conferences = parser_service.get_conferences()

    # Parse date filters if provided
    min_ts = None
    max_ts = None
    if min_date:
        min_ts = int(datetime.strptime(min_date, "%Y-%m-%d").timestamp())
    if max_date:
        max_ts = int(datetime.strptime(max_date, "%Y-%m-%d").timestamp())

    # Filter conferences
    results = []
    for conf in conferences:
        # Apply country filter
        if country:
            conf_country = conf.get("country", "").lower()
            if country.lower() not in conf_country:
                continue

        # Apply date filters
        conf_dates = conf.get("date", {})
        if min_ts is not None or max_ts is not None:
            if not conf_dates:
                continue

            conf_start = conf_dates.get("beginning")
            conf_end = conf_dates.get("end")

            # Check if conference date range overlaps with filter range
            if min_ts is not None and conf_end < min_ts:
                continue
            if max_ts is not None and conf_start > max_ts:
                continue

        # Format date for display
        if conf_dates:
            conf_start = conf_dates.get("beginning")
            conf_end = conf_dates.get("end")
            if conf_start:
                date_str = datetime.fromtimestamp(conf_start).strftime("%Y-%m-%d")
                if conf_end and conf_start != conf_end:
                    end_str = datetime.fromtimestamp(conf_end).strftime("%Y-%m-%d")
                    date_str += f" to {end_str}"
                conf["dateFormatted"] = date_str

        results.append(conf)

    # Sort by date (conferences without dates go to the end)
    results.sort(key=lambda x: x.get("date", {}).get("beginning", float("inf")))

    # Build output
    filters = []
    if min_date:
        filters.append(f"from {min_date}")
    if max_date:
        filters.append(f"until {max_date}")
    if country:
        filters.append(f"in {country}")

    filter_str = " ".join(filters) if filters else "all"
    output = f"Found {len(results)} conferences ({filter_str}):\n\n"

    for c in results:
        output += f"• {c['name']} - {c.get('dateFormatted', 'N/A')}"
        output += f" - {c.get('location', 'N/A')}\n"
        output += f"  {c.get('hyperlink', '')}\n"

    return output


if __name__ == "__main__":
    # Stateless server with JSON responses (recommended)
    mcp.run(transport="streamable-http")
