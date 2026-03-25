import json
from pathlib import Path

CONFIG_DIR = Path.home() / ".feels"
CONFIG_FILE = CONFIG_DIR / "config.json"


def config_exists() -> bool:
    return CONFIG_FILE.exists()


def save_config(config: dict) -> None:
    CONFIG_DIR.mkdir(exist_ok=True)
    CONFIG_FILE.write_text(json.dumps(config, indent=2))


def load_config() -> dict:
    return json.loads(CONFIG_FILE.read_text())
