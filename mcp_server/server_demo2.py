#region Imports
import copy
import json
from datetime import date
from typing import Annotated, Any, Optional

from fastmcp import FastMCP
from fastmcp.server.context import Context
from pydantic import Field

try:
    from .markdown_parser import MarkdownParserService
    from .utils import apply_filter, TALKS_DIR
except ImportError:
    from markdown_parser import MarkdownParserService
    from utils import apply_filter, TALKS_DIR
#endregion

mcp = FastMCP("cfp")

parser_service = MarkdownParserService()

@mcp.tool(
    name="apply_conferences",
    description="Apply to technical conferences matching optional filters and intelligent talk matching.",
)
async def apply_conferences(
    ctx: Context,
    talk_resource_uri: Annotated[
        str,
        Field(description="URI of the talk resource to use for matching (e.g., 'talk://mcp', 'file://...')"),
    ],
    min_date: Annotated[
        Optional[date], Field(description="Minimum conference date (optional)")
    ] = None,
    max_date: Annotated[
        Optional[date], Field(description="Maximum conference date (optional)")
    ] = None,
    country: Annotated[
        Optional[str],
        Field(
            description="Country name to filter (case-insensitive search)"
        ),
    ] = None,
) -> dict[str, Any]:
    #region Récupération des conférences
    conferences = parser_service.get_conferences()
    results = await apply_filter(
        conferences, country=country, max_date=max_date, min_date=min_date, cfp_open=True, tags=None
    )
    conferences_summary = [{
        "name": conf["name"],
        "tags": conf.get("tags", []),
        "location": f"{conf.get('city', 'Unknown')}, {conf.get('country', 'Unknown')}",
    } for conf in results]
    #endregion

    #region Extraction du contenu du talk
    try:
        talk_content = await ctx.read_resource(talk_resource_uri)
        talk_text = str(talk_content.contents[0].content)

        talk_lines = talk_text.split("\n")
        talk_title = talk_lines[0].replace("#", "").strip() if talk_lines else "Unknown talk"

    except Exception as e:
        return {
            "error": f"Unable to read talk resource '{talk_resource_uri}': {str(e)}",
            "matches": [],
        }
    #endregion

    #region Sampling prompt
    sampling_prompt = f"""Analyze which conferences match this talk topic: "{talk_title}"

talk excerpt:
{chr(10).join(talk_lines[:15])}

Available conferences:
{json.dumps(conferences_summary, indent=2, ensure_ascii=False)}

For each conference, evaluate the match based on:
- The conference's tags/themes
- The conference name and theme
- Relevance to the talk topic

Respond ONLY with valid JSON (no markdown, no code blocks):
{{
  "matches": [
    {{
      "name": "exact conference name from the list",
      "score": 0-100,
      "reasoning": "brief explanation in English (max 1 sentence)"
    }}
  ]
}}

Important:
- Only include conferences with score >= 30
- Be strict about tag relevance
- Consider broad themes (e.g., "AI" matches "machine learning", "data science")"""
    #endregion

    #region Sampling and elicitation
    try:
        #region Sampling
        result = await ctx.sample(
            messages=sampling_prompt,
            temperature=0.3,
            max_tokens=4000,
        )

        matches = json.loads(result.text.strip()).get("matches", [])
        #endregion

        #region Elicitation
        applied_confs = []
        for match in matches:
            conf_name = match.get("name", "Unknown")

            prompt = f"Do you want to apply to the CFP for the conference '{conf_name}' with your talk '{talk_title}'?"

            elicit_result = await ctx.elicit(prompt, response_type=None)

            if elicit_result.action == "accept":
                applied_confs.append(conf_name)

        return {
            "talk_uri": talk_resource_uri,
            "talk_title": talk_title,
            "applied_confs": applied_confs,
        }
        #endregion

    except Exception as e:
        return {
            "talk_uri": talk_resource_uri,
            "talk_title": talk_title,
            "error": f"Analysis failed: {str(e)}",
            "applied_confs": [],
        }
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
    mcp.run(transport="streamable-http", host="127.0.0.1", port=8001)
