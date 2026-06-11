from models.base import BaseEntity

class User(BaseEntity):
    _id_counter = 1 

    def __init__(self, name, email, user_id=None):
        super().__init__()
        self.name = name
        self._email = None
        self.email = email
        if user_id is None:
            user_id = f"USR{User._id_counter}"
            User._id_counter += 1
        self.user_id = user_id
        self.projects = []

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, value):
        if '@' not in value or '.' not in value:
            raise ValueError("howdyt! Invalid email format")
        self._email = value

    def to_dict(self):
        return {
            'name': self.name,
            'email': self.email,
            'user_id': self.user_id,
            'projects': [p.to_dict() if hasattr(p, 'to_dict') else p for p in self.projects]
        }

    @classmethod
    def from_dict(cls, data):
        user = cls(data['name'], data['email'], data.get('user_id'))
        return user

    def add_project(self, project):
        self.projects.append(project)

    def display_info(self):
        return f"User: {self.name} | Email: {self.email} | ID: {self.user_id}"

    def __str__(self):
        return f"User: {self.name} ({self.email})"

    def __repr__(self):
        return f"User('{self.name}', '{self.email}', '{self.user_id}')"