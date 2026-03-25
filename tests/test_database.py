import unittest
import tempfile
import sqlite3
from pathlib import Path
from datetime import datetime, timedelta
from unittest.mock import patch, MagicMock
import sys

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))


class TestDatabase(unittest.TestCase):
    """Test suite for database operations."""

    def setUp(self):
        """Create a fresh database for each test."""
        from feels.database import init_db
        from feels.config import CONFIG_FILE

        # Delete existing database and config to start fresh
        db_path = Path.home() / ".feels" / "data.db"
        config_path = Path.home() / ".feels" / "config.json"

        if db_path.exists():
            db_path.unlink()
        if config_path.exists():
            config_path.unlink()

        # Initialize with default config
        self.config = {
            "mood": True,
            "focus": False,
            "stress": False,
            "projects": False,
            "tags": True,
            "note": True,
        }

        init_db(self.config)

    def tearDown(self):
        """Clean up."""
        # Database will be cleaned up in next setUp
        pass

    def test_insert_and_get_log(self):
        """Test inserting and retrieving a log."""
        from feels.database import insert_log, get_log

        entry = {
            "timestamp": datetime.now().isoformat(),
            "mood": 4,
            "tags": "#work #focused",
            "note": "Good progress today",
        }

        log_id = insert_log(entry)
        self.assertEqual(log_id, 1)

        retrieved = get_log(log_id)
        self.assertEqual(retrieved["mood"], 4)
        self.assertEqual(retrieved["tags"], "#work #focused")
        self.assertEqual(retrieved["note"], "Good progress today")

    def test_get_logs_returns_all(self):
        """Test retrieving all logs."""
        from feels.database import insert_log, get_logs

        for i in range(3):
            entry = {
                "timestamp": (datetime.now() - timedelta(days=i)).isoformat(),
                "mood": 3 + i,
                "tags": None,
                "note": f"Log {i+1}",
            }
            insert_log(entry)

        logs = get_logs(all_logs=True, newest_first=False)
        self.assertEqual(len(logs), 3)

    def test_update_log(self):
        """Test updating a log."""
        from feels.database import insert_log, get_log, update_log

        entry = {
            "timestamp": datetime.now().isoformat(),
            "mood": 2,
            "tags": "#tired",
            "note": "Had a rough day",
        }

        log_id = insert_log(entry)

        # Update mood and note
        update_log(log_id, {"mood": 4, "note": "Actually feeling better"})

        updated = get_log(log_id)
        self.assertEqual(updated["mood"], 4)
        self.assertEqual(updated["note"], "Actually feeling better")
        self.assertEqual(updated["tags"], "#tired")

    def test_delete_log(self):
        """Test deleting a log."""
        from feels.database import insert_log, get_log, delete_log

        entry = {
            "timestamp": datetime.now().isoformat(),
            "mood": 3,
            "tags": None,
            "note": None,
        }

        log_id = insert_log(entry)
        delete_log(log_id)

        deleted = get_log(log_id)
        self.assertIsNone(deleted)

    def test_get_stats_basics(self):
        """Test basic statistics calculation."""
        from feels.database import insert_log, get_stats

        insert_log({
            "timestamp": datetime.now().isoformat(),
            "mood": 4,
            "tags": None,
            "note": None,
        })

        stats = get_stats(self.config)
        self.assertEqual(stats["total"], 1)
        self.assertTrue(stats["logged_today"])

    def test_insert_multiple_same_day(self):
        """Test inserting multiple logs on same day."""
        from feels.database import insert_log, get_logs

        today = datetime.now().isoformat()[:10]

        insert_log({
            "timestamp": f"{today}T09:00:00",
            "mood": 2,
            "tags": None,
            "note": None,
        })

        insert_log({
            "timestamp": f"{today}T14:00:00",
            "mood": 4,
            "tags": None,
            "note": None,
        })

        logs = get_logs(all_logs=True, newest_first=False)
        self.assertEqual(len(logs), 2)


class TestDatabaseWithProjects(unittest.TestCase):
    """Test database with projects enabled."""

    def setUp(self):
        """Create a fresh database with projects enabled."""
        from feels.database import init_db

        # Delete existing database and config to start fresh
        db_path = Path.home() / ".feels" / "data.db"
        config_path = Path.home() / ".feels" / "config.json"

        if db_path.exists():
            db_path.unlink()
        if config_path.exists():
            config_path.unlink()

        self.config = {
            "mood": True,
            "focus": False,
            "stress": False,
            "projects": True,
            "tags": True,
            "note": True,
        }

        init_db(self.config)

    def tearDown(self):
        """Clean up."""
        pass

    def test_insert_with_project(self):
        """Test inserting log with project."""
        from feels.database import insert_log, get_log

        entry = {
            "timestamp": datetime.now().isoformat(),
            "mood": 4,
            "project": "feels",
            "tags": "#feature",
            "note": "Implemented stats",
        }

        log_id = insert_log(entry)
        retrieved = get_log(log_id)

        self.assertEqual(retrieved["project"], "feels")
        self.assertEqual(retrieved["mood"], 4)


class TestDatabaseWithOptionalScores(unittest.TestCase):
    """Test database with focus and stress enabled."""

    def setUp(self):
        """Create a fresh database with optional scores."""
        from feels.database import init_db

        # Delete existing database and config to start fresh
        db_path = Path.home() / ".feels" / "data.db"
        config_path = Path.home() / ".feels" / "config.json"

        if db_path.exists():
            db_path.unlink()
        if config_path.exists():
            config_path.unlink()

        self.config = {
            "mood": True,
            "focus": True,
            "stress": True,
            "projects": False,
            "tags": True,
            "note": True,
        }

        init_db(self.config)

    def tearDown(self):
        """Clean up."""
        pass

    def test_insert_with_optional_scores(self):
        """Test inserting log with focus and stress."""
        from feels.database import insert_log, get_log

        entry = {
            "timestamp": datetime.now().isoformat(),
            "mood": 4,
            "focus": 3,
            "stress": 2,
            "tags": "#work",
            "note": "Productive but stressed",
        }

        log_id = insert_log(entry)
        retrieved = get_log(log_id)

        self.assertEqual(retrieved["mood"], 4)
        self.assertEqual(retrieved["focus"], 3)
        self.assertEqual(retrieved["stress"], 2)


if __name__ == "__main__":
    unittest.main()
