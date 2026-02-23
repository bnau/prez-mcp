"""Simple MCP Server implementation."""

import copy
import json
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path
from typing import Annotated, Any, Optional

from fastmcp import FastMCP
from fastmcp.resources import FileResource
from fastmcp.server.context import Context
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
    name="search_conferences",
    description=(
        "Search for technical conferences with optional filters. "
        "Returns structured JSON data. "
        "Filters include date range, country, tags, and CFP status. "
        "Results include conference metadata such as tags, CFP deadlines, and locations. "
        "If match_cfps is True, automatically reads all available CFP files and matches them "
        "with conferences using AI sampling. "
        "Example: search_conferences(min_date='2026-01-01', max_date='2026-12-31', "
        "country='France', tags='python,ai', cfp_open=True, match_cfps=True)"
    ),
)
async def search_conferences(
    ctx: Context,
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
    match_cfps: Annotated[
        Optional[bool],
        Field(
            description=(
                "When True, automatically reads all available CFP files from the server "
                "and matches them with filtered conferences using AI sampling. "
                "Results will be grouped by CFP with match_score (0-100) and reasoning fields. "
                "Returns a dictionary with CFP names as keys and matched conferences as values."
            )
        ),
    ] = False,
    min_score: Annotated[
        Optional[int],
        Field(
            description=(
                "Minimum match score threshold (0-100) when using match_cfps. "
                "Only conferences with score >= min_score will be returned. "
                "Ignored if match_cfps is False."
            ),
            ge=0,
            le=100,
        ),
    ] = 30,
) -> list[Any] | dict[str, Any]:
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

    # Get current timestamp for CFP filtering
    current_ts = int(datetime.now().timestamp())

    # Filter conferences
    results = []
    for conf in conferences:
        # Apply CFP open filter
        if cfp_open:
            cfp = conf.get("cfp")
            if not cfp:
                # No CFP information, skip this conference
                continue
            cfp_deadline = cfp.get("untilDate")
            if not cfp_deadline or cfp_deadline < current_ts:
                # CFP is closed or no deadline, skip this conference
                continue

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

    # If match_cfps is True, read all CFPs and match them with conferences
    if match_cfps:
        # Read all CFP files from the directory
        cfp_matches = {}

        for cfp_file in CFP_SUBJECTS_DIR.glob("*.md"):
            cfp_name = cfp_file.stem
            cfp_content = cfp_file.read_text(encoding="utf-8")

            # Extract CFP title from content (first line without #)
            cfp_lines = cfp_content.split("\n")
            cfp_title = cfp_lines[0].replace("#", "").strip() if cfp_lines else "Unknown CFP"

            # Prepare conferences summary for analysis
            conferences_summary = []
            for conf in results:
                summary = {
                    "name": conf["name"],
                    "tags": conf.get("tags", []),
                    "location": f"{conf.get('city', 'Unknown')}, {conf.get('country', 'Unknown')}",
                }
                conferences_summary.append(summary)

            # Use sampling to analyze matches
            sampling_prompt = f"""Analyze which conferences match this CFP topic: "{cfp_title}"

CFP excerpt:
{chr(10).join(cfp_lines[:10])}

Available conferences:
{json.dumps(conferences_summary, indent=2, ensure_ascii=False)}

For each conference, evaluate the match based on:
- Conference tags/topics
- Conference name and theme
- Relevance to the CFP topic

Respond ONLY with valid JSON (no markdown, no code blocks):
{{
  "matches": [
    {{
      "conference_name": "exact conference name from the list",
      "score": 0-100,
      "reasoning": "brief explanation in French (max 1 sentence)"
    }}
  ]
}}

Important:
- Only include conferences with score >= {min_score}
- Be strict about tag relevance
- Consider broader themes (e.g., "AI" matches "machine learning", "data science")"""

            try:
                # Use FastMCP sampling with ctx
                result = await ctx.sample(
                    messages=sampling_prompt,
                    temperature=0.3,
                    max_tokens=4000,
                )

                # Parse LLM response
                response_text = result.text if result.text else "{}"

                # Clean markdown code blocks if present
                response_text = response_text.strip()
                if response_text.startswith("```"):
                    lines = response_text.split("\n")
                    response_text = "\n".join(lines[1:-1]) if len(lines) > 2 else response_text

                analysis = json.loads(response_text)
                matches = analysis.get("matches", [])

                # Add match scores and reasoning to results for this CFP
                scored_results = []
                for match in matches:
                    conf_name = match.get("conference_name")
                    # Find the corresponding conference in results
                    conf = next((c for c in results if c["name"] == conf_name), None)
                    if conf and match.get("score", 0) >= min_score:
                        # Add match metadata to conference
                        conf_with_score = copy.deepcopy(conf)
                        conf_with_score["match_score"] = match.get("score", 0)
                        conf_with_score["match_reasoning"] = match.get("reasoning", "")
                        scored_results.append(conf_with_score)

                # Sort by match score descending
                scored_results.sort(key=lambda x: x.get("match_score", 0), reverse=True)

                # Pour chaque match, demander à l'utilisateur s'il veut postuler
                for match in scored_results:
                    conf_name = match.get("name", "Unknown")
                    match_score = match.get("match_score", 0)

                    # Utiliser l'élicitation pour demander confirmation
                    prompt = (
                        f"Voulez-vous postuler au CFP de la conférence '{conf_name}' "
                        f"avec votre sujet '{cfp_title}' (score de match: {match_score}/100) ?"
                    )

                    elicit_result = await ctx.elicit(prompt, response_type=bool)

                    # Ajouter le résultat de l'élicitation au match
                    if elicit_result.action == "accept":
                        match["user_wants_to_apply"] = elicit_result.data
                        if elicit_result.data:
                            match["application_status"] = f"✅ Vous allez postuler à '{conf_name}'"
                        else:
                            match["application_status"] = (
                                f"❌ Vous ne postulerez pas à '{conf_name}'"
                            )
                    elif elicit_result.action == "decline":
                        match["user_wants_to_apply"] = None
                        match["application_status"] = "ℹ️ Vous avez décliné de répondre"
                    else:
                        match["user_wants_to_apply"] = None
                        match["application_status"] = "⚠️ Opération annulée"

                # Store matches for this CFP
                cfp_matches[cfp_name] = {
                    "cfp_title": cfp_title,
                    "matches": scored_results,
                }

            except Exception as e:
                # If sampling fails for this CFP, store error
                cfp_matches[cfp_name] = {
                    "cfp_title": cfp_title,
                    "error": f"Failed to analyze matches: {str(e)}",
                    "matches": [],
                }

        return cfp_matches

    # Return as JSON with metadata
    return results


@mcp.prompt(
    name="list_conferences_by_month_and_country",
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


@mcp.prompt(
    name="find_conferences_for_open_cfps",
    description=(
        "Generate a prompt to find technical conferences with open CFPs "
        "and match them with available CFP submissions. This prompt helps identify "
        "the best conferences to submit CFPs to based on topic relevance."
    ),
)
def find_conferences_for_open_cfps(
    country: Annotated[
        Optional[str],
        Field(description="Optional country name to filter conferences (e.g., 'France', 'USA')"),
    ] = None,
) -> str:
    """Generate a prompt to search conferences with open CFPs, optionally filtered by country."""
    country_filter = f" in {country}" if country else ""
    country_param = f"country='{country}'" if country else ""

    return (
        f"Find the best technical conferences{country_filter} with open CFPs "
        "for all available CFP topics.\n\n"
        "Call the search_conferences tool with:\n"
        f"- cfp_open: true{', ' + country_param if country_param else ''}\n"
        "- match_cfps: true\n"
        "- min_score: 30\n\n"
        "This will automatically:\n"
        "1. Filter conferences with open CFPs\n"
        "2. Read all available CFP files from the server\n"
        "3. Match each CFP with relevant conferences using AI\n"
        "4. Return results grouped by CFP with match scores\n\n"
        "Present the results in a clear format showing:\n"
        "- Each CFP name and title\n"
        "- Matching conferences with their scores (0-100)\n"
        "- The reasoning for each match\n"
        "- Conference details (date, location, CFP deadline)\n\n"
        "Use emojis for better readability."
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
