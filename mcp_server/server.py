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
def search_conferences_by_date(start_date: str, end_date: Optional[str] = None) -> str:
    """
    Search for conferences by date range.

    Args:
        start_date: Start date in format YYYY-MM-DD
        end_date: Optional end date in format YYYY-MM-DD (if not provided, uses start_date)

    Returns:
        JSON string with matching conferences
    """
    conferences = parser_service.get_conferences()

    # Parse dates
    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d") if end_date else start

    # Convert to timestamps
    start_ts = int(start.timestamp())
    end_ts = int(end.timestamp())

    # Filter conferences
    results = []
    for conf in conferences:
        conf_dates = conf.get("date", {})
        if conf_dates:
            # Check if conference date falls within range
            conf_start = conf_dates.get("beginning")
            conf_end = conf_dates.get("end")

            if conf_start and conf_end and conf_start <= end_ts and conf_end >= start_ts:
                # Format dates for display
                date_str = datetime.fromtimestamp(conf_start).strftime("%Y-%m-%d")
                if conf_start != conf_end:
                    end_str = datetime.fromtimestamp(conf_end).strftime("%Y-%m-%d")
                    date_str += f" to {end_str}"
                conf["dateFormatted"] = date_str
                results.append(conf)

    output = f"Found {len(results)} conferences:\n\n"
    for c in results[:20]:  # Limit to 20 results
        output += f"• {c['name']} - {c['dateFormatted']}"
        output += f" - {c.get('location', 'N/A')}\n"
        output += f"  {c.get('hyperlink', '')}\n"
    return output


@mcp.tool()
def search_conferences_by_city(city: str) -> str:
    """
    Search for conferences by city name.

    Args:
        city: City name to search for (case-insensitive)

    Returns:
        List of matching conferences
    """
    conferences = parser_service.get_conferences()
    city_lower = city.lower()

    results = []
    for conf in conferences:
        conf_city = conf.get("city", "").lower()
        if city_lower in conf_city:
            # Format date
            conf_dates = conf.get("date", {})
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

    output = f"Found {len(results)} conferences in {city}:\n\n"
    for c in results[:20]:  # Limit to 20 results
        output += f"• {c['name']} - {c.get('dateFormatted', 'N/A')}"
        output += f" - {c.get('location', 'N/A')}\n"
        output += f"  {c.get('hyperlink', '')}\n"
    return output


@mcp.tool()
def search_conferences_by_cfp(
    start_date: Optional[str] = None, end_date: Optional[str] = None
) -> str:
    """
    Search for conferences with open CFPs (Call for Papers).

    Args:
        start_date: Optional CFP deadline start date in format YYYY-MM-DD
        end_date: Optional CFP deadline end date in format YYYY-MM-DD

    Returns:
        List of conferences with open CFPs
    """
    conferences = parser_service.get_conferences()

    results = []
    for conf in conferences:
        cfp = conf.get("cfp", {})
        if cfp and cfp.get("untilDate"):
            cfp_deadline = cfp["untilDate"]

            # If date range provided, filter by CFP deadline
            if start_date or end_date:
                start_ts = 0
                if start_date:
                    start_ts = int(datetime.strptime(start_date, "%Y-%m-%d").timestamp())
                end_ts = float("inf")
                if end_date:
                    end_ts = int(datetime.strptime(end_date, "%Y-%m-%d").timestamp())

                if start_ts <= cfp_deadline <= end_ts:
                    results.append(conf)
            else:
                # No filter, include all with CFP
                results.append(conf)

    # Sort by CFP deadline
    results.sort(key=lambda x: x["cfp"]["untilDate"])

    output = f"Found {len(results)} conferences with CFPs:\n\n"
    for c in results[:20]:  # Limit to 20 results
        cfp_date = datetime.fromtimestamp(c["cfp"]["untilDate"]).strftime("%Y-%m-%d")
        conf_dates = c.get("date", {})
        conf_date = "N/A"
        if conf_dates:
            conf_start = conf_dates.get("beginning")
            if conf_start:
                conf_date = datetime.fromtimestamp(conf_start).strftime("%Y-%m-%d")

        output += f"• {c['name']} - {c.get('location', 'N/A')}\n"
        output += f"  Conference: {conf_date} | CFP Deadline: {cfp_date}\n"
        output += f"  CFP Link: {c['cfp'].get('link', 'N/A')}\n\n"

    return output


if __name__ == "__main__":
    # Stateless server with JSON responses (recommended)
    mcp.run(transport="streamable-http")
