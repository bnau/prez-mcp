"""Unit tests for the MCP server tools."""

from datetime import datetime
from unittest.mock import patch

import pytest

from mcp_server.server import search_conferences


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

            # Should include all conferences with dates
            assert "Found 5 conferences (all)" in result
            assert "PyCon France 2026" in result
            assert "DevOps Days Berlin" in result
            assert "JS Conf USA" in result
            assert "React Summit France" in result
            assert "Conference Without Date" in result

    def test_search_by_country(self, mock_conferences):
        """Test filtering conferences by country."""
        with patch(
            "mcp_server.server.parser_service.get_conferences",
            return_value=mock_conferences,
        ):
            result = search_conferences(country="France")

            assert "Found 2 conferences (in France)" in result
            assert "PyCon France 2026" in result
            assert "React Summit France" in result
            assert "DevOps Days Berlin" not in result
            assert "JS Conf USA" not in result

    def test_search_by_country_case_insensitive(self, mock_conferences):
        """Test country filter is case-insensitive."""
        with patch(
            "mcp_server.server.parser_service.get_conferences",
            return_value=mock_conferences,
        ):
            result = search_conferences(country="france")

            assert "Found 2 conferences" in result
            assert "PyCon France 2026" in result

    def test_search_by_country_partial_match(self, mock_conferences):
        """Test country filter allows partial matches."""
        with patch(
            "mcp_server.server.parser_service.get_conferences",
            return_value=mock_conferences,
        ):
            result = search_conferences(country="Ger")

            assert "Found 1 conference" in result
            assert "DevOps Days Berlin" in result

    def test_search_by_min_date(self, mock_conferences):
        """Test filtering conferences by minimum date."""
        with patch(
            "mcp_server.server.parser_service.get_conferences",
            return_value=mock_conferences,
        ):
            result = search_conferences(min_date="2026-06-01")

            # Should include conferences ending on or after 2026-06-01
            assert "React Summit France" in result  # June 5-6
            assert "JS Conf USA" in result  # August 20-22
            assert "PyCon France 2026" not in result  # May 15-17
            assert "DevOps Days Berlin" not in result  # March 10-11

    def test_search_by_max_date(self, mock_conferences):
        """Test filtering conferences by maximum date."""
        with patch(
            "mcp_server.server.parser_service.get_conferences",
            return_value=mock_conferences,
        ):
            result = search_conferences(max_date="2026-05-31")

            # Should include conferences starting on or before 2026-05-31
            assert "PyCon France 2026" in result  # May 15-17
            assert "DevOps Days Berlin" in result  # March 10-11
            assert "JS Conf USA" not in result  # August 20-22
            assert "React Summit France" not in result  # June 5-6

    def test_search_by_date_range(self, mock_conferences):
        """Test filtering conferences by date range."""
        with patch(
            "mcp_server.server.parser_service.get_conferences",
            return_value=mock_conferences,
        ):
            result = search_conferences(min_date="2026-05-01", max_date="2026-06-30")

            # Should include conferences between May and June
            assert "PyCon France 2026" in result  # May 15-17
            assert "React Summit France" in result  # June 5-6
            assert "DevOps Days Berlin" not in result  # March 10-11
            assert "JS Conf USA" not in result  # August 20-22

    def test_search_by_country_and_date_range(self, mock_conferences):
        """Test combining country and date range filters."""
        with patch(
            "mcp_server.server.parser_service.get_conferences",
            return_value=mock_conferences,
        ):
            result = search_conferences(
                country="France", min_date="2026-06-01", max_date="2026-12-31"
            )

            # Should only include React Summit France (June, in France)
            assert "Found 1 conference" in result
            assert "React Summit France" in result
            assert "PyCon France 2026" not in result  # Too early (May)

    def test_search_filters_conferences_without_dates(self, mock_conferences):
        """Test that conferences without dates are excluded when date filters are applied."""
        with patch(
            "mcp_server.server.parser_service.get_conferences",
            return_value=mock_conferences,
        ):
            result = search_conferences(min_date="2026-01-01")

            # Conference without dates should not be included
            assert "Conference Without Date" not in result

    def test_search_no_results(self, mock_conferences):
        """Test when no conferences match the filters."""
        with patch(
            "mcp_server.server.parser_service.get_conferences",
            return_value=mock_conferences,
        ):
            result = search_conferences(country="Antarctica")

            assert "Found 0 conferences (in Antarctica)" in result

    def test_search_results_sorted_by_date(self, mock_conferences):
        """Test that results are sorted by conference start date."""
        with patch(
            "mcp_server.server.parser_service.get_conferences",
            return_value=mock_conferences,
        ):
            result = search_conferences()

            # Extract conference names in order they appear
            lines = result.split("\n")
            conf_lines = [line for line in lines if line.startswith("•")]

            # Should be sorted chronologically
            assert "DevOps Days Berlin" in conf_lines[0]  # March
            assert "PyCon France 2026" in conf_lines[1]  # May
            assert "React Summit France" in conf_lines[2]  # June
            assert "JS Conf USA" in conf_lines[3]  # August

    def test_search_formats_dates_correctly(self, mock_conferences):
        """Test that dates are formatted correctly in the output."""
        with patch(
            "mcp_server.server.parser_service.get_conferences",
            return_value=mock_conferences,
        ):
            result = search_conferences(country="France")

            # Check date formatting for multi-day conference
            assert "2026-05-15 to 2026-05-17" in result  # PyCon France
            assert "2026-06-05 to 2026-06-06" in result  # React Summit

    def test_search_displays_location_and_link(self, mock_conferences):
        """Test that location and hyperlink are included in output."""
        with patch(
            "mcp_server.server.parser_service.get_conferences",
            return_value=mock_conferences,
        ):
            result = search_conferences(country="Germany")

            assert "Berlin (Germany)" in result
            assert "https://devopsdays.berlin" in result

    def test_search_empty_conference_list(self):
        """Test searching when there are no conferences."""
        with patch("mcp_server.server.parser_service.get_conferences", return_value=[]):
            result = search_conferences()

            assert "Found 0 conferences (all)" in result

    def test_search_filter_description(self, mock_conferences):
        """Test that the filter description is correct."""
        with patch(
            "mcp_server.server.parser_service.get_conferences",
            return_value=mock_conferences,
        ):
            # Test all filter combinations
            result1 = search_conferences()
            assert "(all)" in result1

            result2 = search_conferences(min_date="2026-01-01")
            assert "(from 2026-01-01)" in result2

            result3 = search_conferences(max_date="2026-12-31")
            assert "(until 2026-12-31)" in result3

            result4 = search_conferences(country="France")
            assert "(in France)" in result4

            result5 = search_conferences(
                min_date="2026-01-01", max_date="2026-12-31", country="France"
            )
            assert "(from 2026-01-01 until 2026-12-31 in France)" in result5

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

            assert "Mystery Conference" in result
            assert "N/A" in result  # Should show N/A for missing location

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
            result1 = search_conferences(min_date="2026-03-01", max_date="2026-03-14")
            assert "Found 0 conferences" in result1

            # Search range: March 16-20 (overlaps with conference) - should match
            result2 = search_conferences(min_date="2026-03-16", max_date="2026-03-20")
            assert "Test Conference" in result2

            # Search range: March 18-31 (after conference) - should NOT match
            result3 = search_conferences(min_date="2026-03-18", max_date="2026-03-31")
            assert "Found 0 conferences" in result3

            # Search range: March 10-16 (overlaps start) - should match
            result4 = search_conferences(min_date="2026-03-10", max_date="2026-03-16")
            assert "Test Conference" in result4

            # Search range: March 1-31 (fully contains) - should match
            result5 = search_conferences(min_date="2026-03-01", max_date="2026-03-31")
            assert "Test Conference" in result5
