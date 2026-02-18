"""Parser for extracting conference data from markdown README."""

import re
from datetime import datetime
from pathlib import Path
from typing import Any


class MarkdownParserService:
    """Service for parsing and caching conference data from markdown files."""

    def __init__(self, data_dir: Path | None = None):
        """
        Initialize the parser service.

        Args:
            data_dir: Optional custom data directory path.
                     Defaults to data/developers-conferences-agenda relative to this file.
        """
        if data_dir is None:
            data_dir = Path(__file__).parent.parent / "data" / "developers-conferences-agenda"

        self.data_dir = data_dir
        readme_path = data_dir / "README.md"
        if not readme_path.exists():
            raise FileNotFoundError(
                f"Conference data not found at {readme_path}. "
                "Please ensure the git submodule is initialized: "
                "git submodule update --init --recursive"
            )
        self._conferences = MarkdownParserService.parse_markdown_conferences(self, readme_path)

    def get_conferences(self) -> list[dict[str, Any]]:
        return self._conferences

    def parse_markdown_conferences(self, readme_path: str | Path) -> list[dict[str, Any]]:
        """
        Parse conference data from the developers-conferences-agenda README.md file.

        Args:
            readme_path: Path to the README.md file

        Returns:
            List of conference dictionaries with structured data
        """
        with open(readme_path, encoding="utf-8") as f:
            content = f.read()

        conferences = []
        current_year = None
        current_month = None

        # Split into lines for processing
        lines = content.split("\n")

        for line in lines:
            # Detect year headers (## 2026)
            year_match = re.match(r"^##\s+(\d{4})$", line)
            if year_match:
                current_year = int(year_match.group(1))
                continue

            # Detect month headers (### January)
            month_match = re.match(r"^###\s+(\w+)$", line)
            if month_match:
                current_month = month_match.group(1)
                continue

            # Parse conference entry lines (start with "* ")
            if line.startswith("* ") and current_year and current_month:
                conf = self.parse_conference_line(line, current_year, current_month)
                if conf:
                    conferences.append(conf)

        return conferences

    def parse_conference_line(self, line: str, year: int, month: str) -> dict[str, Any] | None:
        """
        Parse a single conference line from the markdown.

        Format examples:
        * 5-6: [ICSTM 2026](https://waset.org/...) - Bali (Indonesia)
        * 15: [MongoDB.local San Francisco](https://www.mongodb.com/...) - San Francisco, CA (USA)
        * 31-01/02: [FOSDEM 2026](https://fosdem.org/2026/) - Brussels (Belgium)
          <a href="...">CFP...</a>
        """
        # Remove the leading "* "
        line = line[2:].strip()

        # Extract date range (e.g., "5-6:", "15:", "31-01/02:")
        date_match = re.match(r"^([\d\-/]+):\s+", line)
        if not date_match:
            return None

        date_str = date_match.group(1)
        line = line[len(date_match.group(0)) :]

        # Extract conference name and link [Name](URL)
        name_link_match = re.match(r"\[([^\]]+)\]\(([^)]+)\)", line)
        if not name_link_match:
            return None

        name = name_link_match.group(1)
        hyperlink = name_link_match.group(2)
        line = line[len(name_link_match.group(0)) :].strip()

        # Extract location (after " - ")
        location_match = re.match(r"^-\s+([^<\n]+)", line)
        location = "Unknown"
        city = ""
        country = ""

        if location_match:
            location = location_match.group(1).strip()
            line = line[len(location_match.group(0)) :]

            # Parse location (format: "City, State (Country)" or "City (Country)")
            loc_parts = location.rsplit("(", 1)
            if len(loc_parts) == 2:
                city_part = loc_parts[0].strip().rstrip(",")
                country = loc_parts[1].rstrip(")").strip()

                # Handle "City, State" format
                if "," in city_part:
                    city = city_part.split(",")[0].strip()
                else:
                    city = city_part

        # Extract CFP information if present
        cfp_info = None
        cfp_match = re.search(r'<a href="([^"]+)"><img[^>]*message=until%20([^"&]+)', line)
        if cfp_match:
            cfp_link = cfp_match.group(1)
            cfp_date_encoded = cfp_match.group(2)
            # Decode URL-encoded date (e.g., "15-November-2025" or "15-October-2025")
            cfp_date_str = cfp_date_encoded.replace("-", " ")
            try:
                cfp_deadline = datetime.strptime(cfp_date_str, "%d %B %Y")
                cfp_info = {
                    "link": cfp_link,
                    "untilDate": int(cfp_deadline.timestamp()),
                }
            except ValueError:
                # If parsing fails, include CFP link without deadline
                cfp_info = {"link": cfp_link, "untilDate": None}

        # Parse dates into timestamps
        dates = self.parse_date_range(date_str, year, month)

        # Extract tags from the conference name and location
        tags = self.extract_tags(name)

        # Build conference object
        conference = {
            "name": name,
            "date": dates,
            "city": city,
            "country": country,
            "location": location,
            "hyperlink": hyperlink,
            "tags": tags,
        }

        if cfp_info:
            conference["cfp"] = cfp_info

        return conference

    def parse_date_range(self, date_str: str, year: int, month: str) -> dict[str, int]:
        """
        Parse date range string into timestamp dictionary.

        Args:
            date_str: Date string (e.g., "5-6", "15", "31-01/02")
            year: Year as integer
            month: Month name (e.g., "January")

        Returns:
            Dictionary with "beginning" and "end" timestamps in milliseconds

        Examples:
            "5-6" -> {"beginning": timestamp for 5th, "end": timestamp for 6th}
            "15" -> {"beginning": timestamp for 15th, "end": timestamp for 15th}
            "31-01/02" -> {"beginning": timestamp for 31st, "end": timestamp for 2nd of next month}
        """
        month_num = datetime.strptime(month, "%B").month

        # Handle cross-month ranges (e.g., "31-01/02")
        if "-" in date_str and "/" in date_str:
            parts = date_str.split("-")
            start_day = int(parts[0])
            end_part = parts[1]

            # Start date
            start_date = datetime(year, month_num, start_day)
            beginning = int(start_date.timestamp())

            # End date (next month)
            next_month = month_num + 1 if month_num < 12 else 1
            next_year = year if month_num < 12 else year + 1
            end_days = end_part.split("/")
            end_day = int(end_days[0])

            end_date = datetime(next_year, next_month, end_day)
            end = int(end_date.timestamp())

        # Handle same-month ranges (e.g., "5-6")
        elif "-" in date_str:
            parts = date_str.split("-")
            start_day = int(parts[0])
            end_day = int(parts[1])

            start_date = datetime(year, month_num, start_day)
            end_date = datetime(year, month_num, end_day)

            beginning = int(start_date.timestamp())
            end = int(end_date.timestamp())

        # Handle single day (e.g., "15")
        else:
            day = int(date_str)
            date = datetime(year, month_num, day)
            timestamp = int(date.timestamp())
            beginning = timestamp
            end = timestamp

        return {"beginning": beginning, "end": end}

    def extract_tags(self, name: str) -> list[str]:
        """Extract tags based on conference name and location keywords."""
        tags = []
        name_lower = name.lower()

        # Technology keywords
        tech_keywords = {
            "ai": ["ai", "artificial intelligence", "machine learning", "ml"],
            "cloud": ["cloud", "aws", "azure", "gcp"],
            "devops": ["devops", "kubernetes", "docker"],
            "security": ["security", "infosec", "cybersec"],
            "web": ["web", "frontend", "backend", "fullstack"],
            "data": ["data", "database", "analytics", "bigdata"],
            "mobile": ["mobile", "ios", "android"],
            "javascript": ["javascript", "js", "node", "react", "vue", "angular"],
            "python": ["python", "django", "flask"],
            "java": ["java", "spring"],
            ".net": [".net", "dotnet", "csharp", "c#"],
            "agile": ["agile", "scrum"],
            "development": ["voxx", "craft", "gdg", "dev", "developers"],
        }

        for tag, keywords in tech_keywords.items():
            if any(keyword in name_lower for keyword in keywords):
                tags.append(tag)

        return tags
