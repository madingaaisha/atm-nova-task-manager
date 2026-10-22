"""Business logic for ATM Nova Task Manager."""

from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any
from uuid import uuid4

from storage import load_tasks, save_tasks


VALID_PRIORITIES = ("High", "Medium", "Low")


class TaskValidationError(ValueError):
    """Raised when task information is invalid."""


class TaskNotFoundError(LookupError):
    """Raised when a requested task ID does not exist."""


def validate_title(title: str) -> str:
    """Return a cleaned, non-empty task title."""
    cleaned = title.strip()
    if not cleaned:
        raise TaskValidationError("Task title cannot be empty.")
    return cleaned


def validate_priority(priority: str) -> str:
    """Return priority with standard capitalisation."""
    cleaned = priority.strip().casefold()
    matches = {item.casefold(): item for item in VALID_PRIORITIES}
    if cleaned not in matches:
        raise TaskValidationError("Priority must be High, Medium, or Low.")
    return matches[cleaned]


def validate_due_date(due_date: str | None) -> str | None:
    """Validate an optional date in YYYY-MM-DD format."""
    if due_date is None or not due_date.strip():
        return None
    cleaned = due_date.strip()
    try:
        date.fromisoformat(cleaned)
    except ValueError as exc:
        raise TaskValidationError("Due date must be a real date in YYYY-MM-DD format.") from exc
    return cleaned


class TaskManager:
    """Create, query, complete, and delete tasks backed by JSON storage."""

    def __init__(self, data_file: str | Path = "tasks.json") -> None:
        self.data_file = Path(data_file)
        self.tasks: list[dict[str, Any]] = load_tasks(self.data_file)

    def create_task(
        self, title: str, priority: str = "Medium", due_date: str | None = None
    ) -> dict[str, Any]:
        """Create and persist a task, then return it."""
        task = {
            "id": str(uuid4()),
            "title": validate_title(title),
            "priority": validate_priority(priority),
            "due_date": validate_due_date(due_date),
            "completed": False,
            "created_at": datetime.now(timezone.utc).isoformat(),
        }
        self.tasks.append(task)
        self._save()
        return task.copy()

    def list_tasks(self, completed: bool | None = None) -> list[dict[str, Any]]:
        """Return all tasks, or only completed/pending tasks when filtered."""
        selected = self.tasks
        if completed is not None:
            selected = [task for task in self.tasks if task["completed"] is completed]
        return [task.copy() for task in selected]

    def complete_task(self, task_id: str) -> dict[str, Any]:
        """Mark a task as completed and persist the change."""
        task = self._find_task(task_id)
        task["completed"] = True
        self._save()
        return task.copy()

    def delete_task(self, task_id: str) -> dict[str, Any]:
        """Delete a task and return the removed task."""
        task = self._find_task(task_id)
        self.tasks.remove(task)
        self._save()
        return task.copy()

    def _find_task(self, task_id: str) -> dict[str, Any]:
        cleaned_id = task_id.strip()
        for task in self.tasks:
            if task.get("id") == cleaned_id:
                return task
        raise TaskNotFoundError(f"No task found with ID '{cleaned_id}'.")

    def _save(self) -> None:
        save_tasks(self.data_file, self.tasks)

