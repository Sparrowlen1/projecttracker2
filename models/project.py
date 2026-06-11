from models.task import Task
from models.base import BaseEntity

class Project(BaseEntity):
    _id_counter = 1

    def __init__(self, title, description, due_date, project_id=None):
        super().__init__()
        self.title = title
        self.description = description
        self.due_date = due_date
        if project_id is None:
            project_id = f"PRJ{Project._id_counter}"
            Project._id_counter += 1
        self.project_id = project_id
        self.tasks = []

    def to_dict(self):
        return {
            'title': self.title,
            'description': self.description,
            'due_date': self.due_date,
            'project_id': self.project_id,
            'tasks': [t.to_dict() for t in self.tasks]
        }

    @classmethod
    def from_dict(cls, data):
        project = cls(
            data['title'],
            data['description'],
            data['due_date'],
            data.get('project_id')
        )
        for task_data in data.get('tasks', []):
            project.add_task(Task.from_dict(task_data))
        return project

    def add_task(self, task):
        self.tasks.append(task)

    def get_tasks_by_status(self, status):
        return [task for task in self.tasks if task.status == status]

    def display_info(self):
        return f"Howdy! Project: {self.title} | Due: {self.due_date} | Tasks: {len(self.tasks)}"

    def __str__(self):
        return f"Project: {self.title} (Due: {self.due_date})"

    def __repr__(self):
        return f"Project('{self.title}', '{self.description}', '{self.due_date}', '{self.project_id}')"