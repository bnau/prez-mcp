import copy
from datetime import date, datetime
from pathlib import Path
from typing import Any, Optional
from dataclasses import dataclass

TALKS_DIR = Path(__file__).parent  / "talks"

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

async def apply_filter(conferences: list[dict[str, Any]], cfp_open: bool | None, country: str | None,
                       max_date: date | None, min_date: date | None, tags: str | None) -> list[Conference]:
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
    return results
