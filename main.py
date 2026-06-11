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
    def find_project_by_title(self, user, title):
        for project in user.projects:
            if project.title.lower() == title.lower():
                return project
        return None
    def add_project(self, args):
        user = self.find_user_by_name(args.user)
        if not user:
            print(f"howdy Sparrow! User '{args.user}' not found my brother.")
            return
        
        existing_ids = [p.project_id for p in user.projects if p.project_id]
        project_id = generate_id('PRJ', existing_ids)
        
        due_date = format_date(args.due_date)
        project = Project(args.title, args.description, due_date, project_id)
        user.add_project(project)
        self.save_data()
        print(f"howdy Sparrow! Project '{args.title}' added to username: '{user.name}' with ID: {project_id}")
    def list_projects(self, args):
        if args.user:
            user = self.find_user_by_name(args.user)
            if not user:
                print(f"howdy Sparrow! User '{args.user}' not found.")
                return
            
            if not user.projects:
                print(f"howdy Sparrow! User '{user.name}' has no projects.")
                return
            
            headers = ['Project ID', 'Title', 'Description', 'Due Date', 'Tasks']
            rows = []
            for project in user.projects:
                rows.append([project.project_id, project.title, project.description[:30], 
                           project.due_date, len(project.tasks)])
            display_table(f"Projects for {user.name}", headers, rows)
        else:
            all_projects = []
            for user in self.users:
                for project in user.projects:
                    all_projects.append([user.name, project.project_id, project.title, 
                                       project.due_date, len(project.tasks)])
            
            if not all_projects:
                print("howdy Sparrow! No projects found.")
                return
            
            headers = ['User', 'Project ID', 'Title', 'Due Date', 'Tasks']
            display_table('All Projects', headers, all_projects)    
    def search_projects(self, args):
        user = self.find_user_by_name(args.user)
        if not user:
            print(f"howdy Sparrow! User '{args.user}' not found.")
            return
        
        search_term = args.term.lower()
        matching_projects = []
        
        for project in user.projects:
            if search_term in project.title.lower() or search_term in project.description.lower():
                matching_projects.append(project)
        
        if not matching_projects:
            print(f"howdy Sparrow! No projects found matching '{args.term}' for user '{user.name}'.")
            return
        
        headers = ['Project ID', 'Title', 'Description', 'Due Date']
        rows = []
        for project in matching_projects:
            rows.append([project.project_id, project.title, project.description[:30], project.due_date])
        display_table(f"Search Results for '{args.term}'", headers, rows)

    def add_task(self, args):
        task_assigned_to = None
        user = None
        
        for u in self.users:
            project = self.find_project_by_title(u, args.project)
            if project:
                user = u
                break
        
        if not user:
            print(f"howdy Sparrow! Project '{args.project}' not found.")
            return
        
        project = self.find_project_by_title(user, args.project)
        
        existing_ids = [t.task_id for t in project.tasks if t.task_id]
        task_id = generate_id('Task', existing_ids)
        
        task = Task(args.title, task_assigned_to, 'pending', task_id)
        project.add_task(task)
        self.save_data()
        print(f"howdy Sparrow! Task '{args.title}' added to project '{project.title}' with ID: {task_id}")
    
    def complete_task(self, args):
        for user in self.users:
            for project in user.projects:
                for task in project.tasks:
                    if task.title.strip().lower() == args.title.strip().lower():
                        task.mark_complete()
                        self.save_data()
                        print(f"howdy Sparrow! Task '{args.title}' Hereby marked as completed.")
                        return
        
        print(f"howdy Sparrow! Task '{args.title}' not found.")
    
    def list_tasks(self, args):
        user = self.find_user_by_name(args.user)
        if not user:
            print(f"howdy Sparrow! User '{args.user}' not found.")
            return
        
        project = self.find_project_by_title(user, args.project)
        if not project:
            print(f"howdy Sparrow! Project '{args.project}' not found for user '{user.name}'.")
            return
        
        if not project.tasks:
            print(f"howdy Sparrow! Project '{project.title}' has no tasks assigned to him yet.")
            return
        
        headers = ['Task ID', 'Title', 'Status Project']
        rows = []
        for task in project.tasks:
            rows.append([task.task_id, task.title, task.status])
        display_table(f"Tasks for {project.title}", headers, rows)
def main():
    cli = ProjectManagementCLI()
    
    parser = argparse.ArgumentParser(description='howdy Sparrow! Project Management CLI Tool')
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    user_parser = subparsers.add_parser('add-user', help='Add a new user')
    user_parser.add_argument('--name', required=True, help='User name')
    user_parser.add_argument('--email', required=True, help='User email')
    
    list_users_parser = subparsers.add_parser('list-users', help='List all users')

    # subparser
    project_parser = subparsers.add_parser('add-project', help='Add a project to a user')
    project_parser.add_argument('--user', required=True, help='User name')
    project_parser.add_argument('--title', required=True, help='Project title')
    project_parser.add_argument('--description', required=True, help='Project description')
    project_parser.add_argument('--due-date', required=True, help='Project due date')
    
    list_projects_parser = subparsers.add_parser('list-projects', help='List projects')
    list_projects_parser.add_argument('--user', help='Filter by user name')
    
    search_parser = subparsers.add_parser('search-projects', help='Search projects for a user')
    search_parser.add_argument('--user', required=True, help='User name')
    search_parser.add_argument('--term', required=True, help='Search term')

    task_parser = subparsers.add_parser('add-task', help='Add a task to a project')
    task_parser.add_argument('--project', required=True, help='Project title')
    task_parser.add_argument('--title', required=True, help='Task title')
    
    complete_parser = subparsers.add_parser('complete-task', help='Mark a task as complete')
    complete_parser.add_argument('--title', required=True, help='Task title')
    
    list_tasks_parser = subparsers.add_parser('list-tasks', help='List tasks in a project')
    list_tasks_parser.add_argument('--user', required=True, help='User name')
    list_tasks_parser.add_argument('--project', required=True, help='Project title')
    
    args = parser.parse_args()
    
    if args.command == 'add-user':
        cli.add_user(args)
    elif args.command == 'list-users':
        cli.list_users(args)
    elif args.command == 'add-project':
        cli.add_project(args)
    elif args.command == 'list-projects':
        cli.list_projects(args)
    elif args.command == 'search-projects':
        cli.search_projects(args)
    elif args.command == 'add-task':
        cli.add_task(args)
    elif args.command == 'complete-task':
        cli.complete_task(args)
    elif args.command == 'list-tasks':
        cli.list_tasks(args)
    else:
        parser.print_help()
if __name__ == '__main__':
    main()