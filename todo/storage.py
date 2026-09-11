import json
import os
from pathlib import Path
from typing import Any

DEFAULT_PATH = Path.home() / ".todo.json"


def storage_path() -> Path:
    override = os.environ.get("TODO_FILE")
    return Path(override) if override else DEFAULT_PATH


def load(path: Path | None = None) -> list[dict[str, Any]]:
    path = path or storage_path()
    if not path.exists():
        return []
    with path.open(encoding="utf-8") as fh:
        data = json.load(fh)
    if not isinstance(data, list):
        raise TypeError(f"{path} does not contain a list of items")
    return data


def save(items: list[dict[str, Any]], path: Path | None = None) -> None:
    path = path or storage_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as fh:
        json.dump(items, fh, indent=2)
        fh.write("\n")
