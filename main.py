import argparse
from models.user import User
from models.project import Project
from models.task import Task
from utils.file_handler import FileHandler
from utils.helpers import validate_email, format_date, display_table, generate_id

class ProjectManagementCLI:
    def __init__(self):
        self.file_handler = FileHandler()
        self.users = []
        self.load_data()
    
    def load_data(self):
        self.users = self.file_handler.load_data(User, Project, Task)
        if not self.users:
            self.users = []
    
    def save_data(self):
        self.file_handler.save_data(self.users)
    
    def find_user_by_name(self, name):
        for user in self.users:
            if user.name.lower() == name.lower():
                return user
        return None
    
    def find_user_by_id(self, user_id):
        for user in self.users:
            if user.user_id == user_id:
                return user
        return None
    
    def add_user(self, args):
        if not validate_email(args.email):
            print("howdy Sparrow! Invalid email format. Email must contain @ and .")
            return
        
        existing_ids = [u.user_id for u in self.users if u.user_id]
        user_id = generate_id('USR', existing_ids)
        
        user = User(args.name, args.email, user_id)
        self.users.append(user)
        self.save_data()
        print(f"howdy Sparrow! User '{args.name}' added successfully with id: {user_id}")
    
    def list_users(self, args):
        if not self.users:
            print("howdy Sparrow! No users found.")
            return
        
        headers = ['ID', 'Name', 'Email', 'Projects Count']
        rows = []
        for user in self.users:
            rows.append([user.user_id, user.name, user.email, len(user.projects)])
        display_table('Users List', headers, rows)

def main():
    cli = ProjectManagementCLI()
    
    parser = argparse.ArgumentParser(description='howdy Sparrow! Project Management CLI Tool')
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    user_parser = subparsers.add_parser('add-user', help='Add a new user')
    user_parser.add_argument('--name', required=True, help='User name')
    user_parser.add_argument('--email', required=True, help='User email')
    
    list_users_parser = subparsers.add_parser('list-users', help='List all users')
    
    args = parser.parse_args()
    
    if args.command == 'add-user':
        cli.add_user(args)
    elif args.command == 'list-users':
        cli.list_users(args)
    else:
        parser.print_help()

if __name__ == '__main__':
    main()