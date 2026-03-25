import unittest
from pathlib import Path
from datetime import datetime

import sys
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from feels.utils import score_color, format_entry


class TestUtils(unittest.TestCase):
    """Test suite for utility functions."""

    def test_score_color_boundaries(self):
        """Test score_color returns correct colors for boundary values."""
        colors = {
            0: "red",
            1: "dark_orange",
            2: "orange1",
            3: "yellow1",
            4: "chartreuse3",
            5: "green",
        }

        for score, expected_color in colors.items():
            self.assertEqual(score_color(score), expected_color)

    def test_format_entry_basic(self):
        """Test format_entry with basic mood-only config."""
        config = {
            "mood": True,
            "focus": False,
            "stress": False,
            "projects": False,
            "tags": True,
            "note": True,
        }

        entry = {
            "id": 1,
            "timestamp": "2026-03-25T14:30:00",
            "mood": 4,
            "tags": "#work #focused",
            "note": "Made good progress",
        }

        formatted = format_entry(entry, config)
        formatted_str = str(formatted)

        # Check key components are in the formatted output
        self.assertIn("#1", formatted_str)
        self.assertIn("14:30", formatted_str)
        self.assertIn("#work", formatted_str)
        self.assertIn("Made good progress", formatted_str)

    def test_format_entry_with_project(self):
        """Test format_entry with project enabled."""
        config = {
            "mood": True,
            "focus": False,
            "stress": False,
            "projects": True,
            "tags": True,
            "note": True,
        }

        entry = {
            "id": 5,
            "timestamp": "2026-03-25T10:15:00",
            "mood": 3,
            "project": "feels",
            "tags": "#cli",
            "note": "CLI work",
        }

        formatted = format_entry(entry, config)
        formatted_str = str(formatted)

        self.assertIn("#5", formatted_str)
        self.assertIn("feels", formatted_str)
        self.assertIn("#cli", formatted_str)

    def test_format_entry_with_focus_stress(self):
        """Test format_entry with optional scores."""
        config = {
            "mood": True,
            "focus": True,
            "stress": True,
            "projects": False,
            "tags": True,
            "note": True,
        }

        entry = {
            "id": 2,
            "timestamp": "2026-03-25T16:45:00",
            "mood": 5,
            "focus": 4,
            "stress": 1,
            "tags": "#great",
            "note": "Excellent day",
        }

        formatted = format_entry(entry, config)
        formatted_str = str(formatted)

        # All scores should be present
        self.assertIn("5/5", formatted_str)
        self.assertIn("4/5", formatted_str)
        self.assertIn("1/5", formatted_str)

    def test_format_entry_handles_none_values(self):
        """Test format_entry gracefully handles None values."""
        config = {
            "mood": True,
            "focus": False,
            "stress": False,
            "projects": False,
            "tags": True,
            "note": True,
        }

        entry = {
            "id": 3,
            "timestamp": "2026-03-25T09:00:00",
            "mood": 2,
            "tags": None,
            "note": None,
        }

        formatted = format_entry(entry, config)
        formatted_str = str(formatted)

        # Should not crash and should include id/time
        self.assertIn("#3", formatted_str)
        self.assertIn("09:00", formatted_str)

    def test_format_entry_no_tags_or_note(self):
        """Test format_entry when tags and notes are disabled."""
        config = {
            "mood": True,
            "focus": False,
            "stress": False,
            "projects": False,
            "tags": False,
            "note": False,
        }

        entry = {
            "id": 4,
            "timestamp": "2026-03-25T11:30:00",
            "mood": 3,
        }

        formatted = format_entry(entry, config)
        formatted_str = str(formatted)

        # Should still show id and time
        self.assertIn("#4", formatted_str)
        self.assertIn("11:30", formatted_str)

    def test_score_color_invalid_scores(self):
        """Test score_color with out-of-range values."""
        # Scores outside 0-5 should be handled gracefully
        # Assuming implementation clamps or returns a default
        color_high = score_color(10)
        color_low = score_color(-5)

        # Should still return a string (implementation specific)
        self.assertIsInstance(color_high, str)
        self.assertIsInstance(color_low, str)


if __name__ == "__main__":
    unittest.main()
