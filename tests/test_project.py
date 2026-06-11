import unittest
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.project import Project
from models.task import Task

class TestProject(unittest.TestCase):

    def setUp(self):
        self.project = Project(
            title="Test Project",
            description="project fo unit testing",
            due_date="2026-6-18",
            project_id="PRJ999"
        )

    def test_project_creation(self):
        self.assertEqual(self.project.title, "Test Project")
        self.assertEqual(self.project.description, "project fo unit testing")
        self.assertEqual(self.project.due_date, "2026-6-18")
        self.assertEqual(self.project.project_id, "PRJ999")
        self.assertEqual(len(self.project.tasks), 0)

    def test_add_task(self):
        task = Task("Write tests", task_id="TSK101")
        self.project.add_task(task)
        self.assertEqual(len(self.project.tasks), 1)
        self.assertEqual(self.project.tasks[0].title, "Write tests")

    def test_get_tasks_by_status(self):
        task1 = Task("Task pending", status="pending", task_id="TSK1")
        task2 = Task("Task completed", status="completed", task_id="TSK2")
        self.project.add_task(task1)
        self.project.add_task(task2)

        pending = self.project.get_tasks_by_status("pending")
        completed = self.project.get_tasks_by_status("completed")

        self.assertEqual(len(pending), 1)
        self.assertEqual(pending[0].title, "Task pending")
        self.assertEqual(len(completed), 1)
        self.assertEqual(completed[0].title, "Task completed")

    def test_to_dict(self):
        task = Task("Sample task", task_id="TSK55")
        self.project.add_task(task)
        project_dict = self.project.to_dict()

        self.assertEqual(project_dict["title"], "Test Project")
        self.assertEqual(project_dict["project_id"], "PRJ999")
        self.assertEqual(len(project_dict["tasks"]), 1)
        self.assertEqual(project_dict["tasks"][0]["title"], "Sample task")

    def test_from_dict(self):
        data = {
            "title": "Imported Project",
            "description": "Imported from dict",
            "due_date": "2026-01-01",
            "project_id": "PRJ888",
            "tasks": [
                {"title": "Task A", "status": "pending", "task_id": "TSK88", "assigned_to": None}
            ]
        }
        project = Project.from_dict(data)
        self.assertEqual(project.title, "Imported Project")
        self.assertEqual(project.project_id, "PRJ888")
        self.assertEqual(len(project.tasks), 1)
        self.assertEqual(project.tasks[0].title, "Task A")
        self.assertEqual(project.tasks[0].status, "pending")

    def test_str_method(self):
        self.assertEqual(str(self.project), "Project: Test Project (Due: 2026-6-18)")

    def test_repr_method(self):
        expected_repr = "Project('Test Project', 'project fo unit testing', '2026-6-18', 'PRJ999')"
        self.assertEqual(repr(self.project), expected_repr)

    def test_display_info(self):
        info = self.project.display_info()
        self.assertIn("Test Project", info)
        self.assertIn("2026-6-18", info)

if __name__ == "__main__":
    unittest.main()