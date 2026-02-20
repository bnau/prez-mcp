"""Unit tests for the MCP server tools."""

from datetime import date, datetime
from unittest.mock import patch

import pytest

from mcp_server.server import search_conferences, get_cfp, list_conferences_by_month_country


class TestSearchConferences:
    """Tests for the search_conferences tool."""

    @pytest.fixture
    def mock_conferences(self):
        """Create mock conference data for testing."""
        return [
            {
                "name": "PyCon France 2026",
                "city": "Paris",
                "country": "France",
                "location": "Paris (France)",
                "hyperlink": "https://pycon.fr",
                "date": {
                    "beginning": int(datetime(2026, 5, 15).timestamp()),
                    "end": int(datetime(2026, 5, 17).timestamp()),
                },
                "tags": ["python"],
            },
            {
                "name": "DevOps Days Berlin",
                "city": "Berlin",
                "country": "Germany",
                "location": "Berlin (Germany)",
                "hyperlink": "https://devopsdays.berlin",
                "date": {
                    "beginning": int(datetime(2026, 3, 10).timestamp()),
                    "end": int(datetime(2026, 3, 11).timestamp()),
                },
                "tags": ["devops"],
            },
            {
                "name": "JS Conf USA",
                "city": "San Francisco",
                "country": "USA",
                "location": "San Francisco, CA (USA)",
                "hyperlink": "https://jsconf.com",
                "date": {
                    "beginning": int(datetime(2026, 8, 20).timestamp()),
                    "end": int(datetime(2026, 8, 22).timestamp()),
                },
                "tags": ["javascript"],
            },
            {
                "name": "React Summit France",
                "city": "Lyon",
                "country": "France",
                "location": "Lyon (France)",
                "hyperlink": "https://react-summit.fr",
                "date": {
                    "beginning": int(datetime(2026, 6, 5).timestamp()),
                    "end": int(datetime(2026, 6, 6).timestamp()),
                },
                "tags": ["javascript"],
            },
            {
                "name": "Conference Without Date",
                "city": "Nowhere",
                "country": "Noland",
                "location": "Nowhere (Noland)",
                "hyperlink": "https://nodate.com",
                "date": {},
                "tags": [],
            },
        ]

    def test_search_all_conferences(self, mock_conferences):
        """Test searching without any filters returns all conferences."""
        with patch(
            "mcp_server.server.parser_service.get_conferences",
            return_value=mock_conferences,
        ):
            result = search_conferences()

            # Should include all conferences
            assert len(result) == 5

            conf_names = [c["name"] for c in result]
            assert "PyCon France 2026" in conf_names
            assert "DevOps Days Berlin" in conf_names
            assert "JS Conf USA" in conf_names
            assert "React Summit France" in conf_names
            assert "Conference Without Date" in conf_names

    def test_search_by_country(self, mock_conferences):
        """Test filtering conferences by country."""
        with patch(
            "mcp_server.server.parser_service.get_conferences",
            return_value=mock_conferences,
        ):
            result = search_conferences(country="France")

            assert len(result) == 2

            conf_names = [c["name"] for c in result]
            assert "PyCon France 2026" in conf_names
            assert "React Summit France" in conf_names
            assert "DevOps Days Berlin" not in conf_names
            assert "JS Conf USA" not in conf_names

    def test_search_by_country_case_insensitive(self, mock_conferences):
        """Test country filter is case-insensitive."""
        with patch(
            "mcp_server.server.parser_service.get_conferences",
            return_value=mock_conferences,
        ):
            result = search_conferences(country="france")

            assert len(result) == 2

            conf_names = [c["name"] for c in result]
            assert "PyCon France 2026" in conf_names

    def test_search_by_country_partial_match(self, mock_conferences):
        """Test country filter allows partial matches."""
        with patch(
            "mcp_server.server.parser_service.get_conferences",
            return_value=mock_conferences,
        ):
            result = search_conferences(country="Ger")

            assert len(result) == 1

            conf_names = [c["name"] for c in result]
            assert "DevOps Days Berlin" in conf_names

    def test_search_by_min_date(self, mock_conferences):
        """Test filtering conferences by minimum date."""
        with patch(
            "mcp_server.server.parser_service.get_conferences",
            return_value=mock_conferences,
        ):
            result = search_conferences(min_date=date(2026, 6, 1))

            # Should include conferences ending on or after 2026-06-01
            conf_names = [c["name"] for c in result]
            assert "React Summit France" in conf_names  # June 5-6
            assert "JS Conf USA" in conf_names  # August 20-22
            assert "PyCon France 2026" not in conf_names  # May 15-17
            assert "DevOps Days Berlin" not in conf_names  # March 10-11

    def test_search_by_max_date(self, mock_conferences):
        """Test filtering conferences by maximum date."""
        with patch(
            "mcp_server.server.parser_service.get_conferences",
            return_value=mock_conferences,
        ):
            result = search_conferences(max_date=date(2026, 5, 31))

            # Should include conferences starting on or before 2026-05-31
            conf_names = [c["name"] for c in result]
            assert "PyCon France 2026" in conf_names  # May 15-17
            assert "DevOps Days Berlin" in conf_names  # March 10-11
            assert "JS Conf USA" not in conf_names  # August 20-22
            assert "React Summit France" not in conf_names  # June 5-6

    def test_search_by_date_range(self, mock_conferences):
        """Test filtering conferences by date range."""
        with patch(
            "mcp_server.server.parser_service.get_conferences",
            return_value=mock_conferences,
        ):
            result = search_conferences(min_date=date(2026, 5, 1), max_date=date(2026, 6, 30))

            # Should include conferences between May and June
            conf_names = [c["name"] for c in result]
            assert "PyCon France 2026" in conf_names  # May 15-17
            assert "React Summit France" in conf_names  # June 5-6
            assert "DevOps Days Berlin" not in conf_names  # March 10-11
            assert "JS Conf USA" not in conf_names  # August 20-22

    def test_search_by_country_and_date_range(self, mock_conferences):
        """Test combining country and date range filters."""
        with patch(
            "mcp_server.server.parser_service.get_conferences",
            return_value=mock_conferences,
        ):
            result = search_conferences(
                country="France", min_date=date(2026, 6, 1), max_date=date(2026, 12, 31)
            )

            # Should only include React Summit France (June, in France)
            assert len(result) == 1

            conf_names = [c["name"] for c in result]
            assert "React Summit France" in conf_names
            assert "PyCon France 2026" not in conf_names  # Too early (May)

    def test_search_filters_conferences_without_dates(self, mock_conferences):
        """Test that conferences without dates are excluded when date filters are applied."""
        with patch(
            "mcp_server.server.parser_service.get_conferences",
            return_value=mock_conferences,
        ):
            result = search_conferences(min_date=date(2026, 1, 1))

            # Conference without dates should not be included
            conf_names = [c["name"] for c in result]
            assert "Conference Without Date" not in conf_names

    def test_search_no_results(self, mock_conferences):
        """Test when no conferences match the filters."""
        with patch(
            "mcp_server.server.parser_service.get_conferences",
            return_value=mock_conferences,
        ):
            result = search_conferences(country="Antarctica")

            assert len(result) == 0

    def test_search_results_sorted_by_date(self, mock_conferences):
        """Test that results are sorted by conference start date."""
        with patch(
            "mcp_server.server.parser_service.get_conferences",
            return_value=mock_conferences,
        ):
            result = search_conferences()

            # Extract conference names in order they appear
            conf_names = [c["name"] for c in result]

            # Should be sorted chronologically
            assert conf_names[0] == "DevOps Days Berlin"  # March
            assert conf_names[1] == "PyCon France 2026"  # May
            assert conf_names[2] == "React Summit France"  # June
            assert conf_names[3] == "JS Conf USA"  # August

    def test_search_formats_dates_correctly(self, mock_conferences):
        """Test that dates are formatted correctly in the output."""
        with patch(
            "mcp_server.server.parser_service.get_conferences",
            return_value=mock_conferences,
        ):
            result = search_conferences(country="France")

            # Check date formatting for multi-day conference
            pycon = next(c for c in result if c["name"] == "PyCon France 2026")
            assert pycon["date"]["beginning"] == "2026-05-15"
            assert pycon["date"]["end"] == "2026-05-17"

            react = next(c for c in result if c["name"] == "React Summit France")
            assert react["date"]["beginning"] == "2026-06-05"
            assert react["date"]["end"] == "2026-06-06"

    def test_search_displays_location_and_link(self, mock_conferences):
        """Test that location and hyperlink are included in output."""
        with patch(
            "mcp_server.server.parser_service.get_conferences",
            return_value=mock_conferences,
        ):
            result = search_conferences(country="Germany")

            devops = result[0]
            assert devops["location"] == "Berlin (Germany)"
            assert devops["hyperlink"] == "https://devopsdays.berlin"

    def test_search_empty_conference_list(self):
        """Test searching when there are no conferences."""
        with patch("mcp_server.server.parser_service.get_conferences", return_value=[]):
            result = search_conferences()

            assert len(result) == 0

    def test_search_by_tags(self, mock_conferences):
        """Test filtering by tags."""
        with patch(
            "mcp_server.server.parser_service.get_conferences",
            return_value=mock_conferences,
        ):
            result = search_conferences(tags="python")

            assert len(result) == 1

            conf_names = [c["name"] for c in result]
            assert "PyCon France 2026" in conf_names

    def test_search_by_multiple_tags(self, mock_conferences):
        """Test filtering by multiple tags."""
        with patch(
            "mcp_server.server.parser_service.get_conferences",
            return_value=mock_conferences,
        ):
            result = search_conferences(tags="javascript,devops")

            assert len(result) == 3

            conf_names = [c["name"] for c in result]
            assert "JS Conf USA" in conf_names
            assert "React Summit France" in conf_names
            assert "DevOps Days Berlin" in conf_names

    def test_search_handles_conference_without_location(self):
        """Test handling conferences with missing location data."""
        conf = {
            "name": "Mystery Conference",
            "hyperlink": "https://mystery.com",
            "date": {
                "beginning": int(datetime(2026, 4, 1).timestamp()),
                "end": int(datetime(2026, 4, 1).timestamp()),
            },
            "tags": [],
        }

        with patch("mcp_server.server.parser_service.get_conferences", return_value=[conf]):
            result = search_conferences()

            mystery = result[0]
            assert mystery["name"] == "Mystery Conference"

    def test_search_date_overlap_logic(self):
        """Test that date range overlap logic works correctly."""
        # Conference: March 15-17
        conf = {
            "name": "Test Conference",
            "city": "Test City",
            "country": "Test Country",
            "location": "Test City (Test Country)",
            "hyperlink": "https://test.com",
            "date": {
                "beginning": int(datetime(2026, 3, 15).timestamp()),
                "end": int(datetime(2026, 3, 17).timestamp()),
            },
            "tags": [],
        }

        with patch("mcp_server.server.parser_service.get_conferences", return_value=[conf]):
            # Search range: March 1-14 (before conference) - should NOT match
            result1 = search_conferences(min_date=date(2026, 3, 1), max_date=date(2026, 3, 14))
            assert len(result1) == 0

            # Search range: March 16-20 (overlaps with conference) - should match
            result2 = search_conferences(min_date=date(2026, 3, 16), max_date=date(2026, 3, 20))
            conf_names2 = [c["name"] for c in result2]
            assert "Test Conference" in conf_names2

            # Search range: March 18-31 (after conference) - should NOT match
            result3 = search_conferences(min_date=date(2026, 3, 18), max_date=date(2026, 3, 31))
            assert len(result3) == 0

            # Search range: March 10-16 (overlaps start) - should match
            result4 = search_conferences(min_date=date(2026, 3, 10), max_date=date(2026, 3, 16))
            conf_names4 = [c["name"] for c in result4]
            assert "Test Conference" in conf_names4

            # Search range: March 1-31 (fully contains) - should match
            result5 = search_conferences(min_date=date(2026, 3, 1), max_date=date(2026, 3, 31))
            conf_names5 = [c["name"] for c in result5]
            assert "Test Conference" in conf_names5


class TestCFPResources:
    """Tests for CFP resources."""

    def test_get_cfp_mcp_returns_content(self):
        """Test that get_cfp_mcp returns the CFP content."""
        result = get_cfp("mcp")

        assert isinstance(result, str)
        assert len(result) > 0
        assert "MCP en pratique" in result
        assert "Model Context Protocol" in result

    def test_get_cfp_ide_returns_content(self):
        """Test that get_cfp_ide returns the CFP content."""
        result = get_cfp("ide")

        assert isinstance(result, str)
        assert len(result) > 0
        assert "Copilot, Cursor" in result
        assert "assistants de code" in result

    def test_get_cfp_kagent_returns_content(self):
        """Test that get_cfp_kagent returns the CFP content."""
        result = get_cfp("kagent")

        assert isinstance(result, str)
        assert len(result) > 0
        assert "KAgent" in result
        assert "KServe" in result

    def test_cfp_resources_contain_references_section(self):
        """Test that all CFP resources contain a references section."""
        cfp_mcp = get_cfp("mcp")
        cfp_ide = get_cfp("ide")
        cfp_kagent = get_cfp("kagent")

        assert "## Références" in cfp_mcp
        assert "## Références" in cfp_ide
        assert "## Références" in cfp_kagent


class TestPrompts:
    """Tests for MCP prompts."""

    def test_list_conferences_by_month_country_june_france(self):
        """Test the prompt generation for June 2026 in France."""
        result = list_conferences_by_month_country("2026-06", "France")

        assert isinstance(result, str)
        # Check that the prompt contains the expected information
        assert "France" in result
        assert "June 2026" in result
        assert "min_date: 2026-06-01" in result
        assert "max_date: 2026-06-30" in result
        assert "country: France" in result
        assert "search_conferences" in result

    def test_list_conferences_by_month_country_december_usa(self):
        """Test the prompt generation for December 2026 in USA."""
        result = list_conferences_by_month_country("2026-12", "USA")

        assert isinstance(result, str)
        assert "USA" in result
        assert "December 2026" in result
        assert "min_date: 2026-12-01" in result
        assert "max_date: 2026-12-31" in result
        assert "country: USA" in result

    def test_list_conferences_by_month_country_february_leap_year(self):
        """Test the prompt generation for February in a leap year."""
        result = list_conferences_by_month_country("2024-02", "Germany")

        assert isinstance(result, str)
        assert "Germany" in result
        assert "February 2024" in result
        assert "min_date: 2024-02-01" in result
        assert "max_date: 2024-02-29" in result  # Leap year

    def test_list_conferences_by_month_country_february_non_leap_year(self):
        """Test the prompt generation for February in a non-leap year."""
        result = list_conferences_by_month_country("2026-02", "Spain")

        assert isinstance(result, str)
        assert "Spain" in result
        assert "February 2026" in result
        assert "min_date: 2026-02-01" in result
        assert "max_date: 2026-02-28" in result  # Non-leap year

    def test_list_conferences_by_month_country_formatting_instructions(self):
        """Test that the prompt includes formatting instructions."""
        result = list_conferences_by_month_country("2026-07", "Japan")

        # Check for table formatting instructions
        assert "table" in result.lower()
        assert "Conference Name" in result
        assert "Date" in result
        assert "City" in result
        assert "Tags" in result
        assert "CFP Deadline" in result
        assert "Website Link" in result

    def test_list_conferences_by_month_country_suggestion_for_no_results(self):
        """Test that the prompt includes suggestion for no results."""
        result = list_conferences_by_month_country("2026-03", "Canada")

        assert "no conferences are found" in result.lower()
        assert "suggest" in result.lower()
