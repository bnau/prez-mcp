#region Imports
from datetime import date
from pathlib import Path
from typing import Annotated, Any, Optional

from fastmcp import FastMCP
from fastmcp.resources import FileResource
from pydantic import Field, AnyUrl

try:
    from .markdown_parser import MarkdownParserService
    from .utils import apply_filter, TALKS_DIR
except ImportError:
    from markdown_parser import MarkdownParserService
    from utils import apply_filter, TALKS_DIR
#endregion

mcp = FastMCP("cfp")

parser_service = MarkdownParserService()

#region MCP tool
@mcp.tool(
    name="search_conferences",
    description=(
            "Search for technical conferences with optional filters. "
            "Returns structured JSON data. "
            "Filters include date range, country, tags, and CFP status. "
            "Results include conference metadata such as tags, CFP deadlines, and locations. "
            "Example: search_conferences(min_date='2026-01-01', max_date='2026-12-31', "
            "country='France', tags='python,ai', cfp_open=True)"
    ),
)
async def search_conferences(
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
        cfp_open: Annotated[
            Optional[bool],
            Field(
                description=(
                        "Optional filter to only show conferences with open CFPs. "
                        "When True, only returns conferences where the CFP deadline is in the future. "
                        "When False or None, returns all conferences regardless of CFP status."
                )
            ),
        ] = False,
) -> list[Any]:
    conferences = parser_service.get_conferences()

    return await apply_filter(conferences, cfp_open, country, max_date, min_date, tags)
#endregion

#region MCP Prompt
@mcp.prompt(
    name="list_conferences_by_month_and_country",
    description="List technical conferences by month and country",
)
def list_conferences_by_month_country(
        month: Annotated[
            Optional[int],
            Field(description="Month number"),
        ] = None,
        country: Annotated[
            Optional[str],
            Field(description="Country name"),
        ] = None,
) -> str:
    year = date.today().year

    if month and country:
        return f"Search for technical conferences in {country} during month {month} of {year}."
    elif month:
        return f"Search for technical conferences during month {month} of {year}."
    elif country:
        return f"Search for technical conferences in {country}."
    else:
        return "Search for technical conferences."
#endregion

#region MCP resources
for f in list(TALKS_DIR.glob("*.md")):
    path = Path(TALKS_DIR / f"{f.stem}.md").resolve()
    if path.exists():
        resource = FileResource(
            uri=AnyUrl(f"file://{path.as_posix()}"),
            path=path,
            name=f.stem,
            mime_type="text/markdown",
        )
        mcp.add_resource(resource)
#endregion

#region MCP templated resource
@mcp.resource(
    uri="talk://{theme}",
    name="Talk Content by Theme",
    description="Read talk content for a given theme. Example: read_resource('talk://mcp')",
    mime_type="text/markdown",
)
def get_talk(theme: str) -> str:
    talk_file = TALKS_DIR / f"{theme}.md"
    if talk_file.exists():
        return talk_file.read_text(encoding="utf-8")
    return "Talk not found"
#endregion


if __name__ == "__main__":
    mcp.run(transport="streamable-http", host="127.0.0.1", port=8000)
