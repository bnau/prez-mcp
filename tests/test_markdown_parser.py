"""Unit tests for the markdown parser module."""

import tempfile
from datetime import datetime
from pathlib import Path

import pytest

from mcp_server.markdown_parser import MarkdownParserService


class TestParseDateRange:
    """Tests for the parse_date_range function."""

    def setup_method(self):
        """Setup method to initialize the parser service."""
        self.parser = MarkdownParserService()

    def test_single_day(self):
        """Test parsing a single day."""
        result = self.parser.parse_date_range("15", 2026, "January")
        assert "beginning" in result
        assert "end" in result
        # January 15, 2026 - both beginning and end should be the same
        expected = datetime(2026, 1, 15)
        expected_ts = int(expected.timestamp())
        assert result["beginning"] == expected_ts
        assert result["end"] == expected_ts

    def test_same_month_range(self):
        """Test parsing a range within the same month."""
        result = self.parser.parse_date_range("5-6", 2026, "January")
        assert "beginning" in result
        assert "end" in result
        # January 5, 2026
        start_date = datetime(2026, 1, 5)
        # January 6, 2026
        end_date = datetime(2026, 1, 6)
        assert result["beginning"] == int(start_date.timestamp())
        assert result["end"] == int(end_date.timestamp())

    def test_cross_month_range(self):
        """Test parsing a range that crosses into the next month."""
        result = self.parser.parse_date_range("31-01/02", 2026, "January")
        assert "beginning" in result
        assert "end" in result
        # January 31, 2026
        start_date = datetime(2026, 1, 31)
        # February 2, 2026
        end_date = datetime(2026, 2, 1)
        assert result["beginning"] == int(start_date.timestamp())
        assert result["end"] == int(end_date.timestamp())

    def test_cross_year_range(self):
        """Test parsing a range that crosses into the next year."""
        result = self.parser.parse_date_range("31-01/01", 2026, "December")
        assert "beginning" in result
        assert "end" in result
        # December 31, 2026
        start_date = datetime(2026, 12, 31)
        # January 2, 2027
        end_date = datetime(2027, 1, 1)
        assert result["beginning"] == int(start_date.timestamp())
        assert result["end"] == int(end_date.timestamp())


class TestExtractTags:
    """Tests for the extract_tags function."""

    def setup_method(self):
        """Setup method to initialize the parser service."""
        self.parser = MarkdownParserService()

    def test_ai_keywords(self):
        """Test extraction of AI-related tags."""
        tags = self.parser.extract_tags("AI Conference 2026")
        assert "ai" in tags

        tags = self.parser.extract_tags("Machine Learning Summit")
        assert "ai" in tags

    def test_cloud_keywords(self):
        """Test extraction of cloud-related tags."""
        tags = self.parser.extract_tags("AWS Summit")
        assert "cloud" in tags

        tags = self.parser.extract_tags("Cloud Native Days")
        assert "cloud" in tags

    def test_devops_keywords(self):
        """Test extraction of DevOps-related tags."""
        tags = self.parser.extract_tags("DevOps Conference")
        assert "devops" in tags

        tags = self.parser.extract_tags("Kubernetes Summit")
        assert "devops" in tags

    def test_security_keywords(self):
        """Test extraction of security-related tags."""
        tags = self.parser.extract_tags("InfoSec Conference")
        assert "security" in tags

        tags = self.parser.extract_tags("CyberSec Summit")
        assert "security" in tags

    def test_javascript_keywords(self):
        """Test extraction of JavaScript-related tags."""
        tags = self.parser.extract_tags("React Conference")
        assert "javascript" in tags

        tags = self.parser.extract_tags("Node.js Summit")
        assert "javascript" in tags

    def test_python_keywords(self):
        """Test extraction of Python-related tags."""
        tags = self.parser.extract_tags("Python Conference 2026")
        assert "python" in tags

        tags = self.parser.extract_tags("Django Conference")
        assert "python" in tags

    def test_development_keywords(self):
        """Test extraction of development-related tags."""
        tags = self.parser.extract_tags("DevFest Nantes")
        assert "development" in tags

        tags = self.parser.extract_tags("Devoxx France")
        assert "development" in tags

    def test_multiple_tags(self):
        """Test extraction of multiple tags from one conference."""
        tags = self.parser.extract_tags("JavaScript AI Conference")
        assert "javascript" in tags
        assert "ai" in tags

    def test_no_matching_tags(self):
        """Test when no tags match."""
        tags = self.parser.extract_tags("Generic Tech Conference")
        assert len(tags) == 0


class TestParseConferenceLine:
    """Tests for the parse_conference_line function."""

    def setup_method(self):
        """Setup method to initialize the parser service."""
        self.parser = MarkdownParserService()

    def test_basic_conference_line(self):
        """Test parsing a basic conference line."""
        line = "* 5-6: [ICSTM 2026](https://waset.org/conf) - Bali (Indonesia)"
        result = self.parser.parse_conference_line(line, 2026, "January")

        assert result is not None
        assert result["name"] == "ICSTM 2026"
        assert result["hyperlink"] == "https://waset.org/conf"
        assert result["city"] == "Bali"
        assert result["country"] == "Indonesia"
        assert result["location"] == "Bali (Indonesia)"
        assert "beginning" in result["date"]
        assert "end" in result["date"]

    def test_conference_with_state(self):
        """Test parsing a conference with city and state."""
        line = "* 15: [MongoDB.local](https://mongodb.com) - San Francisco, CA (USA)"
        result = self.parser.parse_conference_line(line, 2026, "January")

        assert result is not None
        assert result["name"] == "MongoDB.local"
        assert result["city"] == "San Francisco"
        assert result["country"] == "USA"
        assert result["location"] == "San Francisco, CA (USA)"

    def test_conference_with_cfp(self):
        """Test parsing a conference with CFP information."""
        line = (
            "* 10-11: [Test Conf](https://test.com) - Paris (France) "
            '<a href="https://cfp.test.com"><img alt="CFP" '
            'src="https://img.shields.io/static/v1?label=CFP&'
            'message=until%2015-November-2025&color=red"></a>'
        )
        result = self.parser.parse_conference_line(line, 2026, "January")

        assert result is not None
        assert "cfp" in result
        assert result["cfp"]["link"] == "https://cfp.test.com"
        assert result["cfp"]["untilDate"] is not None

        # Check the CFP deadline is November 15, 2025
        cfp_date = datetime.fromtimestamp(result["cfp"]["untilDate"])
        assert cfp_date.year == 2025
        assert cfp_date.month == 11
        assert cfp_date.day == 15

    def test_conference_with_invalid_cfp_date(self):
        """Test parsing a conference with invalid CFP date format."""
        line = (
            "* 10-11: [Test Conf](https://test.com) - Paris (France) "
            '<a href="https://cfp.test.com"><img alt="CFP" '
            'src="https://img.shields.io/static/v1?label=CFP&'
            'message=until%20InvalidDate&color=red"></a>'
        )
        result = self.parser.parse_conference_line(line, 2026, "January")

        assert result is not None
        assert "cfp" in result
        assert result["cfp"]["link"] == "https://cfp.test.com"
        assert result["cfp"]["untilDate"] is None

    def test_conference_with_cross_month_dates(self):
        """Test parsing a conference that spans two months."""
        line = "* 31-01/02: [FOSDEM 2026](https://fosdem.org/2026/) - Brussels (Belgium)"
        result = self.parser.parse_conference_line(line, 2026, "January")

        assert result is not None
        assert result["name"] == "FOSDEM 2026"
        assert "beginning" in result["date"]
        assert "end" in result["date"]

        # Check dates span from January 31 to February 2
        start_date = datetime.fromtimestamp(result["date"]["beginning"])
        end_date = datetime.fromtimestamp(result["date"]["end"])

        assert start_date.month == 1
        assert start_date.day == 31
        assert end_date.month == 2
        assert end_date.day == 1

    def test_invalid_line_no_date(self):
        """Test that lines without dates return None."""
        line = "* [Invalid Conference](https://invalid.com) - City (Country)"
        result = self.parser.parse_conference_line(line, 2026, "January")
        assert result is None

    def test_invalid_line_no_link(self):
        """Test that lines without proper links return None."""
        line = "* 15: Invalid Conference - City (Country)"
        result = self.parser.parse_conference_line(line, 2026, "January")
        assert result is None

    def test_conference_with_tags_in_name(self):
        """Test that tags are extracted from conference name."""
        line = "* 15: [JavaScript AI Summit](https://js-ai.com) - Berlin (Germany)"
        result = self.parser.parse_conference_line(line, 2026, "May")

        assert result is not None
        assert "javascript" in result["tags"]
        assert "ai" in result["tags"]


class TestParseMarkdownConferences:
    """Tests for the parse_markdown_conferences function."""

    def setup_method(self):
        """Setup method to initialize the parser service."""
        self.parser = MarkdownParserService()

    def test_parse_empty_file(self):
        """Test parsing an empty markdown file."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
            f.write("")
            temp_path = f.name

        try:
            result = self.parser.parse_markdown_conferences(temp_path)
            assert result == []
        finally:
            Path(temp_path).unlink()

    def test_parse_file_with_no_conferences(self):
        """Test parsing a markdown file without conference entries."""
        content = """
# Title

Some text here.

## 2026

### January

No conference entries here, just text.
"""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
            f.write(content)
            temp_path = f.name

        try:
            result = self.parser.parse_markdown_conferences(temp_path)
            assert result == []
        finally:
            Path(temp_path).unlink()

    def test_parse_file_with_single_conference(self):
        """Test parsing a markdown file with one conference."""
        content = """
## 2026

### January

* 15: [Test Conference](https://test.com) - Paris (France)
"""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
            f.write(content)
            temp_path = f.name

        try:
            result = self.parser.parse_markdown_conferences(temp_path)
            assert len(result) == 1
            assert result[0]["name"] == "Test Conference"
            assert result[0]["city"] == "Paris"
            assert result[0]["country"] == "France"
        finally:
            Path(temp_path).unlink()

    def test_parse_file_with_multiple_conferences(self):
        """Test parsing a markdown file with multiple conferences."""
        content = """
## 2026

### January

* 15: [Conf A](https://a.com) - City A (Country A)
* 20: [Conf B](https://b.com) - City B (Country B)

### February

* 10: [Conf C](https://c.com) - City C (Country C)
"""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
            f.write(content)
            temp_path = f.name

        try:
            result = self.parser.parse_markdown_conferences(temp_path)
            assert len(result) == 3
            assert result[0]["name"] == "Conf A"
            assert result[1]["name"] == "Conf B"
            assert result[2]["name"] == "Conf C"

            # Check dates are in different months
            date_a = datetime.fromtimestamp(result[0]["date"]["beginning"])
            date_c = datetime.fromtimestamp(result[2]["date"]["beginning"])
            assert date_a.month == 1
            assert date_c.month == 2
        finally:
            Path(temp_path).unlink()

    def test_parse_file_with_multiple_years(self):
        """Test parsing a markdown file with conferences in multiple years."""
        content = """
## 2025

### December

* 25: [Conf 2025](https://2025.com) - City (Country)

## 2026

### January

* 15: [Conf 2026](https://2026.com) - City (Country)
"""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
            f.write(content)
            temp_path = f.name

        try:
            result = self.parser.parse_markdown_conferences(temp_path)
            assert len(result) == 2

            # Check years are correct
            date_2025 = datetime.fromtimestamp(result[0]["date"]["beginning"])
            date_2026 = datetime.fromtimestamp(result[1]["date"]["beginning"])
            assert date_2025.year == 2025
            assert date_2026.year == 2026
        finally:
            Path(temp_path).unlink()

    def test_parse_file_with_cfp(self):
        """Test parsing a markdown file with CFP information."""
        content = """
## 2026

### January

* 15: [Conf With CFP](https://conf.com) - Paris (France) <a href="https://cfp.com"><img alt="CFP" src="https://img.shields.io/static/v1?label=CFP&message=until%2010-December-2025&color=red"></a>
"""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
            f.write(content)
            temp_path = f.name

        try:
            result = self.parser.parse_markdown_conferences(temp_path)
            assert len(result) == 1
            assert "cfp" in result[0]
            assert result[0]["cfp"]["link"] == "https://cfp.com"

            # Check CFP deadline
            cfp_date = datetime.fromtimestamp(result[0]["cfp"]["untilDate"])
            assert cfp_date.year == 2025
            assert cfp_date.month == 12
            assert cfp_date.day == 10
        finally:
            Path(temp_path).unlink()

    def test_parse_file_mixed_valid_invalid_lines(self):
        """Test parsing a file with both valid and invalid conference lines."""
        content = """
## 2026

### January

* 15: [Valid Conf](https://valid.com) - Paris (France)
* This is not a valid conference line
* Invalid without link - Paris (France)
* 20: [Another Valid](https://valid2.com) - Berlin (Germany)
"""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
            f.write(content)
            temp_path = f.name

        try:
            result = self.parser.parse_markdown_conferences(temp_path)
            # Should only parse valid conferences
            assert len(result) == 2
            assert result[0]["name"] == "Valid Conf"
            assert result[1]["name"] == "Another Valid"
        finally:
            Path(temp_path).unlink()

    def test_parse_real_world_format(self):
        """Test parsing with realistic conference entry format."""
        content = (
            """
# Developers Conferences Agenda

## 2026

### January

* 5-6: [ICSTM 2026](https://waset.org/conference) - Bali (Indonesia)
* 6-9: [CES](https://www.ces.tech) - Las Vegas, NV (USA)
* 14-17: [SnowCamp 2026](https://snowcamp.io/) - Grenoble (France) """
            + (
                '<a href="https://conference-hall.io/snowcamp-2026">'
                '<img alt="CFP SnowCamp" '
                'src="https://img.shields.io/static/v1?label=CFP&'
                'message=until%2015-October-2025&color=red"></a>'
            )
            + """

### February

* 3: [Cloud Native Days](https://cloudnativedays.fr/) - Paris (France)
"""
        )
        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
            f.write(content)
            temp_path = f.name

        try:
            result = self.parser.parse_markdown_conferences(temp_path)
            assert len(result) == 4

            # Check first conference
            assert result[0]["name"] == "ICSTM 2026"
            assert result[0]["city"] == "Bali"
            assert len(result[0]["date"]) == 2

            # Check conference with state
            assert result[1]["name"] == "CES"
            assert result[1]["city"] == "Las Vegas"

            # Check conference with CFP
            assert result[2]["name"] == "SnowCamp 2026"
            assert "cfp" in result[2]
            assert result[2]["cfp"]["link"] == "https://conference-hall.io/snowcamp-2026"

            # Check tags extraction
            assert "cloud" in result[3]["tags"]
        finally:
            Path(temp_path).unlink()


class TestEdgeCases:
    """Tests for edge cases and error handling."""

    def setup_method(self):
        """Setup method to initialize the parser service."""
        self.parser = MarkdownParserService()

    def test_parse_nonexistent_file(self):
        """Test that parsing a non-existent file raises an error."""
        with pytest.raises(FileNotFoundError):
            self.parser.parse_markdown_conferences("/nonexistent/path/to/file.md")

    def test_parse_conference_line_with_special_characters(self):
        """Test parsing conference names with special characters."""
        line = "* 15: [Conf & Summit - AI/ML](https://test.com) - Paris (France)"
        result = self.parser.parse_conference_line(line, 2026, "March")

        assert result is not None
        assert result["name"] == "Conf & Summit - AI/ML"

    def test_parse_conference_line_with_unicode(self):
        """Test parsing conference with unicode characters."""
        line = "* 15: [Conférence Français](https://test.com) - Montréal (Canada)"
        result = self.parser.parse_conference_line(line, 2026, "June")

        assert result is not None
        assert result["name"] == "Conférence Français"
        assert result["city"] == "Montréal"

    def test_parse_date_range_leap_year(self):
        """Test parsing dates around leap year."""
        # February 29 exists in 2024 (leap year)
        result = self.parser.parse_date_range("28-29", 2024, "February")
        assert "beginning" in result
        assert "end" in result

        date_28 = datetime.fromtimestamp(result["beginning"])
        date_29 = datetime.fromtimestamp(result["end"])

        assert date_28.day == 28
        assert date_29.day == 29
        assert date_29.month == 2
