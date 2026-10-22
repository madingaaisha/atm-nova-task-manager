# ATM Nova Task Manager

A beginner-friendly command-line task manager built for ATM Nova Technologies. It uses only Python 3.12's standard library and stores tasks locally in JSON.

## Features

- Add tasks with High, Medium, or Low priority
- Add an optional due date in `YYYY-MM-DD` format
- View all, pending, or completed tasks
- Complete and safely delete tasks using unique IDs
- Automatically save and reload data from `tasks.json`
- Handle invalid input, missing tasks, and empty lists clearly

## Run on Windows PowerShell

From the workspace:

```powershell
cd C:\Users\AISHA\ATM-Nova-Technologies\00-starter-task-manager
.\.venv\Scripts\Activate.ps1
python .\app.py
```

If PowerShell blocks activation, the virtual environment can be used directly:

```powershell
.\.venv\Scripts\python.exe .\app.py
```

The app creates `tasks.json` after the first task is added. That personal data file is ignored by Git.

## Run the tests

```powershell
cd C:\Users\AISHA\ATM-Nova-Technologies\00-starter-task-manager
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

Tests use temporary directories, never the real `tasks.json` file.

## Project files

- `app.py`: menu, prompts, and output—the command-line interface.
- `task_manager.py`: task rules and reusable operations.
- `storage.py`: JSON loading and safe saving.
- `tests/`: automated tests for expected and invalid cases.
- `ARCHITECTURE.md`: a simple tour of the design.
- `.gitignore`: keeps generated, private, and secret files out of Git.

There is no `requirements.txt` because this application has no external dependencies.

## Python concepts

A **function** is a named block of reusable work. For example, `validate_due_date()` receives text, checks it, and returns a valid date string. Calling a function avoids repeating the same logic.

A **class** is a blueprint that groups related data and behaviour. `TaskManager` holds the current task list and offers methods such as `create_task()`, `list_tasks()`, `complete_task()`, and `delete_task()`.

**JSON** is a readable text format for structured data. A Python list of task dictionaries is converted to JSON when saved and converted back when loaded. The storage layer writes a temporary file first, reducing the chance of leaving a half-written data file.

A **virtual environment** gives this project its own isolated Python setup. It prevents packages from one project interfering with another. This project currently needs no packages, but using `.venv` establishes a good workflow for future growth.

## Git basics

Git records snapshots called commits. `git add` selects changes for the next snapshot; `git commit` records them locally with a message. The repository has no remote publication step: pushing to GitHub should happen only after explicit approval.

## Future AI integration

The menu is separate from `TaskManager`, so an AI assistant can later import and call the same task methods instead of pretending to type into the menu. A future tool adapter could validate an AI request, call `create_task()` or another method, and return the result. No AI framework or paid service is needed for that design today.

