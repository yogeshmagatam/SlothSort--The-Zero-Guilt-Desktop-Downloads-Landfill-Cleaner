import os
import yaml
from pathlib import Path
from typing import Dict, Any

DEFAULT_CONFIG_PATH = Path(__file__).resolve().parent.parent / "config.yaml"

def load_config(config_path: str = None) -> Dict[str, Any]:
    path = Path(config_path) if config_path else DEFAULT_CONFIG_PATH
    if not path.exists():
        raise FileNotFoundError(f"Config file not found at: {path}")
    with open(path, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)
    config["watch_directories"] = [str(Path(p).expanduser().resolve()) for p in config.get("watch_directories", [])]
    config["destination_base"] = str(Path(config.get("destination_base", "~/Documents/SlothSorted")).expanduser().resolve())
    return config
