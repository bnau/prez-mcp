"""Simple MCP Server implementation."""

import copy
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path
from typing import Annotated, Any, Optional

from mcp.server.fastmcp import FastMCP
from mcp.server.fastmcp.resources import FileResource
from pydantic import Field

try:
    from .markdown_parser import MarkdownParserService
except ImportError:
    # When running as script directly
    from markdown_parser import MarkdownParserService

# Create server instance
mcp = FastMCP("cfp-server")

# Initialize the markdown parser service
parser_service = MarkdownParserService()

# CFP subjects directory
CFP_SUBJECTS_DIR = Path(__file__).parent.parent / "prez" / "sujets_cfp"


@dataclass
class Conference:
    name: str
    date: dict[str, Optional[str]]  # {'beginning': 'YYYY-MM-DD', 'end': 'YYYY-MM-DD'}
    location: Optional[str]
    country: Optional[str]
    city: Optional[str]
    tags: list[str]
    cfp: Optional[dict[str, Optional[str]]]  # {'until': 'YYYY-MM-DD', ...}
    hyperlink: Optional[str]


@mcp.tool(
    name="Search Conferences",
    description=(
        "Search for technical conferences with optional filters. "
        "Returns structured JSON data. "
        "Filters include date range, country, and tags. "
        "Results include conference metadata such as tags, CFP deadlines, and locations. "
        "Example: search_conferences(min_date='2026-01-01', max_date='2026-12-31', "
        "country='France', tags='python,ai')"
    ),
)
def search_conferences(
    min_date: Annotated[
        Optional[date], Field(description="Optional minimum conference date")
    ] = None,
    max_date: Annotated[
        Optional[date], Field(description="Optional maximum conference date")
    ] = None,
    country: Annotated[
        Optional[str],
        Field(
            description=(
                "Optional country name to filter by (case-insensitive partial match), "
                "example: 'France', 'USA', 'UK', 'India'..."
            )
        ),
    ] = None,
    tags: Annotated[
        Optional[str],
        Field(
            description=(
                "Optional comma-separated list of tags to filter by "
                "(e.g., 'ai,cloud,devops,security,web,data,mobile,"
                "javascript,python,java,.net,agile,development')"
            )
        ),
    ] = None,
) -> list[Any]:
    conferences = parser_service.get_conferences()

    # Parse date filters if provided
    min_ts = None
    max_ts = None
    if min_date:
        min_ts = int(datetime.combine(min_date, datetime.min.time()).timestamp())
    if max_date:
        max_ts = int(datetime.combine(max_date, datetime.max.time()).timestamp())

    # Parse tags filter if provided
    tag_filters = []
    if tags:
        tag_filters = [tag.strip().lower() for tag in tags.split(",")]

    # Filter conferences
    results = []
    for conf in conferences:
        # Apply country filter
        if country:
            conf_country = conf.get("country", "").lower()
            if country.lower() not in conf_country:
                continue

        # Apply tags filter
        if tag_filters:
            conf_tags = [tag.lower() for tag in conf.get("tags", [])]
            # Check if any of the requested tags match
            if not any(tag_filter in conf_tags for tag_filter in tag_filters):
                continue

        # Apply date filters
        conf_dates = conf.get("date", {})
        if min_ts is not None or max_ts is not None:
            if not conf_dates:
                continue

            conf_start = conf_dates.get("beginning")
            conf_end = conf_dates.get("end")

            # Skip if dates are not timestamps (already formatted)
            if not isinstance(conf_start, (int, float)) or not isinstance(conf_end, (int, float)):
                continue

            # Check if conference date range overlaps with filter range
            if min_ts is not None and conf_end < min_ts:
                continue
            if max_ts is not None and conf_start > max_ts:
                continue

        # Create a copy and add formatted dates
        conf_copy = copy.deepcopy(conf)
        # Keep original timestamps for sorting
        original_beginning = None
        if conf_dates:
            conf_start = conf_dates.get("beginning")
            conf_end = conf_dates.get("end")
            original_beginning = conf_start
            # Add formatted dates to the existing date object
            if conf_start:
                conf_copy["date"]["beginning"] = datetime.fromtimestamp(conf_start).strftime(
                    "%Y-%m-%d"
                )
            if conf_end:
                conf_copy["date"]["end"] = datetime.fromtimestamp(conf_end).strftime("%Y-%m-%d")

        # Store original timestamp for sorting
        conf_copy["_sort_key"] = original_beginning if original_beginning else float("inf")

        # Format CFP deadline if present
        if conf_copy.get("cfp") and conf_copy["cfp"].get("untilDate"):
            cfp_ts = conf_copy["cfp"]["untilDate"]
            if cfp_ts:
                conf_copy["cfp"]["untilDate"] = datetime.fromtimestamp(cfp_ts).strftime("%Y-%m-%d")

        results.append(conf_copy)

    # Sort by date (conferences without dates go to the end)
    results.sort(key=lambda x: x.get("_sort_key", float("inf")))

    # Remove sorting helper field
    for conf in results:
        conf.pop("_sort_key", None)

    # Return as JSON with metadata
    return results


@mcp.prompt(
    name="List Conferences by Month and Country",
    description=(
        "Generate a prompt to list all technical conferences in a specific month and "
        "country. This prompt helps users discover conferences happening in their "
        "desired location and time frame."
    ),
)
def list_conferences_by_month_country(
    month: Annotated[
        str,
        Field(description="Month in YYYY-MM format (e.g., '2026-06', '2026-12')"),
    ],
    country: Annotated[
        str,
        Field(description="Country name (e.g., 'France', 'USA', 'Germany')"),
    ],
) -> str:
    """Generate a prompt to search conferences by month and country."""
    # Extract year and month from the input
    year, month_num = month.split("-")

    # Calculate first and last day of the month
    from calendar import monthrange

    last_day = monthrange(int(year), int(month_num))[1]
    min_date = f"{year}-{month_num}-01"
    max_date = f"{year}-{month_num}-{last_day:02d}"

    # Map month number to month name
    month_names = {
        "01": "January",
        "02": "February",
        "03": "March",
        "04": "April",
        "05": "May",
        "06": "June",
        "07": "July",
        "08": "August",
        "09": "September",
        "10": "October",
        "11": "November",
        "12": "December",
    }
    month_name = month_names.get(month_num, month_num)

    return (
        f"Please search for all technical conferences happening in {country} "
        f"during {month_name} {year}. Use the search_conferences tool with the "
        f"following parameters:\n"
        f"- min_date: {min_date}\n"
        f"- max_date: {max_date}\n"
        f"- country: {country}\n\n"
        f"Then, format the results in a clear table with the following columns:\n"
        f"- Conference Name\n"
        f"- Date (start - end)\n"
        f"- City\n"
        f"- Tags\n"
        f"- CFP Deadline (if available)\n"
        f"- Website Link\n\n"
        f"If no conferences are found, suggest nearby months or countries with "
        f"similar tech events."
    )


@mcp.resource(
    uri="cfp://{theme}",
    name="CFP Content by Theme",
    description=("Read CFP content for a given theme. Example: read_resource('cfp://mcp')"),
    mime_type="text/markdown",
)
def get_cfp(theme: str) -> str:
    cfp_file = CFP_SUBJECTS_DIR / f"{theme}.md"
    if cfp_file.exists():
        return cfp_file.read_text(encoding="utf-8")
    return "CFP not found"


for f in list(CFP_SUBJECTS_DIR.glob("*.md")):
    path = Path(CFP_SUBJECTS_DIR / f"{f.stem}.md").resolve()
    if path.exists():
        resource = FileResource(
            uri=f"file://{path.as_posix()}",
            path=path,
            name=f.stem,
            mime_type="text/markdown",
        )
        mcp.add_resource(resource)

if __name__ == "__main__":
    # Stateless server with JSON responses (recommended)
    mcp.run(transport="streamable-http")
