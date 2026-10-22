"""JSON persistence helpers for ATM Nova Task Manager."""

import json
from pathlib import Path
from typing import Any


class StorageError(Exception):
    """Raised when task data cannot be read or written safely."""


def load_tasks(file_path: str | Path) -> list[dict[str, Any]]:
    """Load tasks from *file_path*, returning an empty list if it is absent."""
    path = Path(file_path)
    if not path.exists():
        return []

    try:
        with path.open("r", encoding="utf-8") as file:
            data = json.load(file)
    except (OSError, json.JSONDecodeError) as exc:
        raise StorageError(f"Could not load tasks from {path}: {exc}") from exc

    if not isinstance(data, list) or not all(isinstance(item, dict) for item in data):
        raise StorageError(f"Task data in {path} must be a JSON list of objects.")
    return data


def save_tasks(file_path: str | Path, tasks: list[dict[str, Any]]) -> None:
    """Save tasks as readable JSON, using a temporary file for safer writes."""
    path = Path(file_path)
    temporary_path = path.with_suffix(path.suffix + ".tmp")

    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        with temporary_path.open("w", encoding="utf-8") as file:
            json.dump(tasks, file, indent=2, ensure_ascii=False)
            file.write("\n")
        temporary_path.replace(path)
    except OSError as exc:
        raise StorageError(f"Could not save tasks to {path}: {exc}") from exc

