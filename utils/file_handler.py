import json
import os

class FileHandler:
    def __init__(self, filepath='data/storage.json'):
        self.filepath = filepath
        self.ensure_data_directory()
    
    def ensure_data_directory(self):
        directory = os.path.dirname(self.filepath)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)
    
    def save_data(self, users):
        data = [user.to_dict() for user in users]
        try:
            with open(self.filepath, 'w') as f:
                json.dump(data, f, indent=4)
            return True
        except Exception as e:
            print(f"howdyt! Error saving data: {e}")
            return False
    
    def load_data(self, user_class, project_class, task_class):
        if not os.path.exists(self.filepath):
            return []
        
        try:
            with open(self.filepath, 'r') as f:
                data = json.load(f)
            
            users = []
            for user_data in data:
                user = user_class.from_dict(user_data)
                for project_data in user_data.get('projects', []):
                    project = project_class.from_dict(project_data)
                    user.add_project(project)
                users.append(user)
            return users
        except Exception as e:
            print(f"howdyt! Error loading data: {e}")
            return []