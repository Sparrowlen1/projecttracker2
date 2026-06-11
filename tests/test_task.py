import unittest
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.task import Task

class TestTask(unittest.TestCase):

    def setUp(self):
        self.task = Task(
            title="Setup environment",
            assigned_to="developer",
            status="pending",
            task_id="TSK001"
        )

    def test_task_creation(self):
        self.assertEqual(self.task.title, "Setup environment")
        self.assertEqual(self.task.assigned_to, "developer")
        self.assertEqual(self.task.status, "pending")
        self.assertEqual(self.task.task_id, "TSK001")

    def test_mark_complete(self):
        self.task.mark_complete()
        self.assertEqual(self.task.status, "completed")

    def test_status_setter_valid(self):
        self.task.status = "in_progress"
        self.assertEqual(self.task.status, "in_progress")
        self.task.status = "completed"
        self.assertEqual(self.task.status, "completed")

    def test_status_setter_invalid(self):
        with self.assertRaises(ValueError):
            self.task.status = "invalid_status"

    def test_to_dict(self):
        task_dict = self.task.to_dict()
        self.assertEqual(task_dict["title"], "Setup environment")
        self.assertEqual(task_dict["assigned_to"], "developer")
        self.assertEqual(task_dict["status"], "pending")
        self.assertEqual(task_dict["task_id"], "TSK001")

    def test_from_dict(self):
        data = {
            "title": "Write documentation",
            "assigned_to": "writer",
            "status": "pending",
            "task_id": "TSK999"
        }
        task = Task.from_dict(data)
        self.assertEqual(task.title, "Write documentation")
        self.assertEqual(task.assigned_to, "writer")
        self.assertEqual(task.status, "pending")
        self.assertEqual(task.task_id, "TSK999")

    def test_str_method(self):
        self.assertEqual(str(self.task), "Task: Setup environment [pending]")

    def test_repr_method(self):
        expected = "Task('Setup environment', 'developer', 'pending', 'TSK001')"
        self.assertEqual(repr(self.task), expected)

    def test_display_info(self):
        info = self.task.display_info()
        self.assertIn("Setup environment", info)
        self.assertIn("pending", info)

if __name__ == "__main__":
    unittest.main()
    