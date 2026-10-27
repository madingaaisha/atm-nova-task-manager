"""Command-line interface for ATM Nova Task Manager."""

from pathlib import Path

from storage import StorageError
from task_manager import TaskManager, TaskNotFoundError, TaskValidationError


DATA_FILE = Path(__file__).with_name("tasks.json")


def display_tasks(
    tasks: list[dict], heading: str, empty_message: str = "No tasks to show."
) -> None:
    """Print a readable task list."""
    print(f"\n{heading}")
    print("-" * len(heading))
    if not tasks:
        print(empty_message)
        return

    for task in tasks:
        status = "Completed" if task["completed"] else "Pending"
        due = task["due_date"] or "No due date"
        print(f"[{status}] {task['title']}")
        print(f"  ID: {task['id']}")
        print(f"  Priority: {task['priority']} | Due: {due}")


def view_tasks(
    manager: TaskManager,
    heading: str,
    completed: bool | None = None,
    empty_message: str = "No tasks to show.",
) -> None:
    """Display a task category and wait so the user can read the result."""
    tasks = manager.list_tasks(completed=completed)
    display_tasks(tasks, heading, empty_message)
    input("\nPress Enter to return to the main menu...")


def choose_task_id(manager: TaskManager, prompt: str) -> str | None:
    """Show tasks and ask for an ID, returning None when there are no tasks."""
    tasks = manager.list_tasks()
    display_tasks(tasks, "All tasks")
    if not tasks:
        return None
    return input(prompt).strip()


def add_task(manager: TaskManager) -> None:
    title = input("Task title: ")
    priority = input("Priority (High/Medium/Low) [Medium]: ").strip() or "Medium"
    due_date = input("Due date (YYYY-MM-DD, optional): ")
    task = manager.create_task(title, priority, due_date)
    print(f"Task added with ID {task['id']}.")


def complete_task(manager: TaskManager) -> None:
    task_id = choose_task_id(manager, "Enter the task ID to complete: ")
    if task_id is not None:
        task = manager.complete_task(task_id)
        print(f"Completed: {task['title']}")


def delete_task(manager: TaskManager) -> None:
    task_id = choose_task_id(manager, "Enter the task ID to delete: ")
    if task_id is None:
        return
    answer = input("Delete this task? (y/N): ").strip().casefold()
    if answer not in {"y", "yes"}:
        print("Deletion cancelled.")
        return
    task = manager.delete_task(task_id)
    print(f"Deleted: {task['title']}")


def print_menu() -> None:
    print("\nATM Nova Task Manager")
    print("=" * 21)
    print("1. Add a task")
    print("2. View all tasks")
    print("3. View pending tasks")
    print("4. View completed tasks")
    print("5. Mark a task as completed")
    print("6. Delete a task")
    print("7. Exit")


def main() -> None:
    """Run the interactive application."""
    try:
        manager = TaskManager(DATA_FILE)
    except StorageError as exc:
        print(f"Unable to start: {exc}")
        return

    actions = {
        "1": lambda: add_task(manager),
        "2": lambda: view_tasks(
            manager, "All tasks", empty_message="There are no tasks yet."
        ),
        "3": lambda: view_tasks(
            manager,
            "Pending tasks",
            completed=False,
            empty_message="There are no pending tasks.",
        ),
        "4": lambda: view_tasks(
            manager,
            "Completed tasks",
            completed=True,
            empty_message="There are no completed tasks.",
        ),
        "5": lambda: complete_task(manager),
        "6": lambda: delete_task(manager),
    }

    while True:
        print_menu()
        choice = input("Choose an option (1-7): ").strip()
        if choice == "7":
            print("Goodbye!")
            break
        action = actions.get(choice)
        if action is None:
            print("Invalid choice. Please enter a number from 1 to 7.")
            continue
        try:
            action()
        except (TaskValidationError, TaskNotFoundError, StorageError) as exc:
            print(f"Error: {exc}")


if __name__ == "__main__":
    main()

