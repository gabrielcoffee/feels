import unittest
import tempfile
import json
from pathlib import Path
from unittest.mock import patch

import sys
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from feels.config import config_exists, load_config, save_config


class TestConfig(unittest.TestCase):
    """Test suite for configuration management."""

    def setUp(self):
        """Create a temporary directory for config files."""
        self.temp_dir = tempfile.TemporaryDirectory()
        self.temp_path = Path(self.temp_dir.name)

        # Mock CONFIG_DIR and CONFIG_FILE paths
        self.config_dir_patcher = patch("feels.config.CONFIG_DIR", self.temp_path)
        self.config_file_patcher = patch(
            "feels.config.CONFIG_FILE", self.temp_path / "config.json"
        )

        self.config_dir_patcher.start()
        self.config_file_patcher.start()

    def tearDown(self):
        """Clean up temporary files."""
        self.config_dir_patcher.stop()
        self.config_file_patcher.stop()
        self.temp_dir.cleanup()

    def test_config_exists_false_when_not_created(self):
        """Test config_exists returns False when no config file exists."""
        self.assertFalse(config_exists())

    def test_save_config(self):
        """Test saving configuration to file."""
        config = {
            "mood": True,
            "focus": False,
            "stress": True,
            "projects": False,
            "tags": True,
            "note": True,
            "active_projects": [],
        }

        save_config(config)

        # Config file should exist
        self.assertTrue((self.temp_path / "config.json").exists())

    def test_config_exists_true_after_save(self):
        """Test config_exists returns True after saving."""
        config = {
            "mood": True,
            "focus": False,
            "stress": False,
            "projects": False,
            "tags": True,
            "note": True,
        }

        save_config(config)
        self.assertTrue(config_exists())

    def test_load_config(self):
        """Test loading configuration from file."""
        original_config = {
            "mood": True,
            "focus": True,
            "stress": False,
            "projects": True,
            "tags": True,
            "note": True,
            "active_projects": ["feels", "other"],
            "last_project": "feels",
        }

        save_config(original_config)
        loaded_config = load_config()

        # Verify all fields are loaded correctly
        self.assertEqual(loaded_config["mood"], True)
        self.assertEqual(loaded_config["focus"], True)
        self.assertEqual(loaded_config["stress"], False)
        self.assertEqual(loaded_config["projects"], True)
        self.assertIn("feels", loaded_config.get("active_projects", []))

    def test_save_and_load_roundtrip(self):
        """Test save and load are consistent."""
        original_config = {
            "mood": True,
            "focus": False,
            "stress": True,
            "projects": True,
            "tags": True,
            "note": True,
            "active_projects": ["project1", "project2"],
            "last_project": "project1",
        }

        save_config(original_config)
        loaded_config = load_config()

        # All fields should match
        for key in original_config:
            self.assertEqual(loaded_config.get(key), original_config[key])

    def test_config_file_is_json(self):
        """Test that config file is valid JSON."""
        config = {
            "mood": True,
            "focus": False,
            "stress": False,
            "projects": False,
            "tags": True,
            "note": True,
        }

        save_config(config)

        # Read file directly and parse JSON
        with open(self.temp_path / "config.json") as f:
            json_config = json.load(f)

        self.assertEqual(json_config["mood"], True)

    def test_load_config_with_missing_optional_fields(self):
        """Test loading config with missing optional fields."""
        # Create a minimal config file without optional fields
        config_file = self.temp_path / "config.json"
        minimal_config = {
            "mood": True,
            "focus": False,
            "stress": False,
            "projects": False,
            "tags": True,
            "note": True,
        }

        with open(config_file, "w") as f:
            json.dump(minimal_config, f)

        loaded_config = load_config()

        # Should load successfully
        self.assertTrue(loaded_config["mood"])
        # Optional fields may be missing
        self.assertEqual(loaded_config.get("active_projects"), None)

    def test_save_preserves_all_field_types(self):
        """Test that save/load preserves various data types."""
        config = {
            "mood": True,
            "focus": False,
            "stress": True,
            "projects": True,
            "tags": True,
            "note": True,
            "active_projects": ["p1", "p2", "p3"],
            "last_project": "p1",
        }

        save_config(config)
        loaded = load_config()

        # Booleans should remain booleans
        self.assertIsInstance(loaded["mood"], bool)
        self.assertIsInstance(loaded["focus"], bool)

        # Lists should remain lists
        self.assertIsInstance(loaded["active_projects"], list)

        # Strings should remain strings
        self.assertIsInstance(loaded["last_project"], str)


if __name__ == "__main__":
    unittest.main()
