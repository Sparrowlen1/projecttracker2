from models.base import BaseEntity

class Task(BaseEntity):
    _id_counter = 1

    def __init__(self, title, assigned_to=None, status='pending', task_id=None):
        super().__init__()
        self.title = title
        self.assigned_to = assigned_to
        self._status = None
        self.status = status 
        if task_id is None:
            task_id = f"TSK{Task._id_counter}"
            Task._id_counter += 1
        self.task_id = task_id

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        valid_statuses = ['pending', 'in_progress', 'completed']
        if value not in valid_statuses:
            raise ValueError(f"howdyt! Status must be one of {valid_statuses}")
        self._status = value

    def to_dict(self):
        return {
            'title': self.title,
            'assigned_to': self.assigned_to,
            'status': self.status,
            'task_id': self.task_id
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            data['title'],
            data.get('assigned_to'),
            data.get('status', 'pending'),
            data.get('task_id')
        )

    def mark_complete(self):
        self.status = 'completed'

    def display_info(self):
        return f"Task: {self.title} | Status: {self.status} | Assigned to: {self.assigned_to}"

    def __str__(self):
        return f"Task: {self.title} [{self.status}]"

    def __repr__(self):
        return f"Task('{self.title}', '{self.assigned_to}', '{self.status}', '{self.task_id}')"