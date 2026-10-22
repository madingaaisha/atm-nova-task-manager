# Architecture

ATM Nova Task Manager is split into three small layers so each part has one clear job.

```text
User
  |
  v
app.py (menu and input/output)
  |
  v
task_manager.py (validation and task operations)
  |
  v
storage.py (read/write JSON) ---> tasks.json
```

## Command-line layer: `app.py`

This file displays the menu, gathers user input, and prints friendly results. It does not directly edit JSON. Deletion confirmation belongs here because it is a user-interface concern.

## Business-logic layer: `task_manager.py`

`TaskManager` owns the in-memory list of tasks. Its public methods are intentionally reusable:

- `create_task(title, priority, due_date)`
- `list_tasks(completed)`
- `complete_task(task_id)`
- `delete_task(task_id)`

Validation functions reject blank titles, unknown priorities, and impossible or incorrectly formatted dates. UUIDs provide stable unique task identifiers.

## Storage layer: `storage.py`

`load_tasks()` reads JSON and returns an empty list when no data file exists. `save_tasks()` writes readable JSON through a temporary file and then replaces the destination. Storage failures become clear `StorageError` exceptions.

## Data shape

Each task is a dictionary similar to:

```json
{
  "id": "a-unique-uuid",
  "title": "Learn Python",
  "priority": "High",
  "due_date": "2026-11-01",
  "completed": false,
  "created_at": "2026-10-22T10:00:00+00:00"
}
```

## Testing

`unittest` tests business and storage behaviour independently of the interactive menu. Every test creates a temporary directory, so personal task data is never touched.

## Growth path

A future AI-agent adapter can import `TaskManager` and translate structured AI tool calls into its public methods. Other interfaces—such as a web API—can do the same without rewriting validation or persistence.
