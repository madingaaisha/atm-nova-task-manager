import json
import tempfile
import unittest
from pathlib import Path

from storage import StorageError, load_tasks
from task_manager import TaskManager, TaskNotFoundError, TaskValidationError


class TaskManagerTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.data_file = Path(self.temporary_directory.name) / "tasks.json"
        self.manager = TaskManager(self.data_file)

    def tearDown(self) -> None:
        self.temporary_directory.cleanup()

    def test_creating_task_sets_expected_values_and_unique_ids(self) -> None:
        first = self.manager.create_task("Learn Python", "high", "2026-11-01")
        second = self.manager.create_task("Write tests", "Low")
        self.assertEqual(first["title"], "Learn Python")
        self.assertEqual(first["priority"], "High")
        self.assertEqual(first["due_date"], "2026-11-01")
        self.assertFalse(first["completed"])
        self.assertNotEqual(first["id"], second["id"])

    def test_saving_and_reloading_tasks(self) -> None:
        created = self.manager.create_task("Persistent task")
        reloaded_manager = TaskManager(self.data_file)
        self.assertEqual(reloaded_manager.list_tasks()[0]["id"], created["id"])

    def test_completing_task(self) -> None:
        task = self.manager.create_task("Finish project")
        completed = self.manager.complete_task(task["id"])
        self.assertTrue(completed["completed"])
        self.assertEqual(len(self.manager.list_tasks(completed=True)), 1)
        self.assertEqual(self.manager.list_tasks(completed=False), [])

    def test_deleting_task(self) -> None:
        task = self.manager.create_task("Temporary task")
        removed = self.manager.delete_task(task["id"])
        self.assertEqual(removed["id"], task["id"])
        self.assertEqual(self.manager.list_tasks(), [])
        self.assertEqual(load_tasks(self.data_file), [])

    def test_priority_validation(self) -> None:
        with self.assertRaisesRegex(TaskValidationError, "Priority"):
            self.manager.create_task("Task", "Urgent")

    def test_due_date_validation(self) -> None:
        invalid_dates = ("01/12/2026", "2026-02-30", "tomorrow")
        for invalid_date in invalid_dates:
            with self.subTest(invalid_date=invalid_date):
                with self.assertRaisesRegex(TaskValidationError, "Due date"):
                    self.manager.create_task("Task", due_date=invalid_date)

    def test_empty_title_is_rejected(self) -> None:
        with self.assertRaisesRegex(TaskValidationError, "cannot be empty"):
            self.manager.create_task("   ")

    def test_empty_task_list_and_missing_file_are_handled(self) -> None:
        self.assertEqual(self.manager.list_tasks(), [])
        self.assertEqual(load_tasks(self.data_file), [])

    def test_invalid_task_id_is_rejected(self) -> None:
        with self.assertRaises(TaskNotFoundError):
            self.manager.complete_task("missing-id")
        with self.assertRaises(TaskNotFoundError):
            self.manager.delete_task("missing-id")

    def test_invalid_json_is_reported(self) -> None:
        self.data_file.write_text("not json", encoding="utf-8")
        with self.assertRaises(StorageError):
            TaskManager(self.data_file)

    def test_non_list_json_is_reported(self) -> None:
        self.data_file.write_text(json.dumps({"title": "wrong shape"}), encoding="utf-8")
        with self.assertRaises(StorageError):
            TaskManager(self.data_file)


if __name__ == "__main__":
    unittest.main()

