import unittest
import sys
import os
import json
import tempfile
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.file_handler import FileHandler
from models.user import User
from models.project import Project
from models.task import Task

class TestFileHandler(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.test_file = os.path.join(self.temp_dir.name, "test_storage.json")
        self.file_handler = FileHandler(self.test_file)

        # Create sample users
        self.user1 = User("Alice", "alice@test.com", "USR99")
        self.user2 = User("Bob", "bob@test.com", "USR100")

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_save_and_load_empty(self):
        """Test saving and loading empty user list"""
        self.file_handler.save_data([])
        loaded = self.file_handler.load_data(User, Project, Task)
        self.assertEqual(loaded, [])

    def test_save_and_load_users_without_projects(self):
        """Test saving and loading users without projects"""
        users = [self.user1, self.user2]
        self.file_handler.save_data(users)
        loaded = self.file_handler.load_data(User, Project, Task)

        self.assertEqual(len(loaded), 2)
        self.assertEqual(loaded[0].name, "Alice")
        self.assertEqual(loaded[0].email, "alice@test.com")
        self.assertEqual(loaded[0].user_id, "USR99")
        self.assertEqual(loaded[1].name, "Bob")

    def test_save_and_load_with_projects_and_tasks(self):
        """Test saving and loading nested data"""
        project = Project("Test Project", "Description", "2026-12-31", "PRJ777")
        task = Task("Test Task", status="pending", task_id="TSK555")
        project.add_task(task)
        self.user1.add_project(project)

        users = [self.user1]
        self.file_handler.save_data(users)
        loaded = self.file_handler.load_data(User, Project, Task)

        self.assertEqual(len(loaded), 1)
        loaded_user = loaded[0]
        self.assertEqual(loaded_user.name, "Alice")
        self.assertEqual(len(loaded_user.projects), 1)

        loaded_project = loaded_user.projects[0]
        self.assertEqual(loaded_project.title, "Test Project")
        self.assertEqual(loaded_project.project_id, "PRJ777")
        self.assertEqual(len(loaded_project.tasks), 1)

        loaded_task = loaded_project.tasks[0]
        self.assertEqual(loaded_task.title, "Test Task")
        self.assertEqual(loaded_task.status, "pending")
        self.assertEqual(loaded_task.task_id, "TSK555")

    def test_load_missing_file(self):
        """Test loading when file does not exist"""
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
        loaded = self.file_handler.load_data(User, Project, Task)
        self.assertEqual(loaded, []) 

    def test_load_corrupted_json(self):
        """Test loading a malformed JSON file"""
        with open(self.test_file, 'w') as f:
            f.write("This is not valid JSON")
        loaded = self.file_handler.load_data(User, Project, Task)
        self.assertEqual(loaded, []) 

    def test_ensure_data_directory(self):
        """Test that directory is created automatically"""
        deep_path = os.path.join(self.temp_dir.name, "subdir", "nested", "storage.json")
        handler = FileHandler(deep_path)
        self.assertTrue(os.path.exists(os.path.dirname(deep_path)))

if __name__ == "__main__":
    unittest.main()