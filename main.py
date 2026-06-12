import argparse
from models.user import User
from models.project import Project
from models.task import Task
from utils.file_handler import FileHandler
from utils.helpers import validate_email, format_date, display_table, generate_id
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

class ProjectManagementCLI:
    def __init__(self):
        logging.debug("Howdy Sparrow we are initalizing the project management CLI...")
        self.file_handler = FileHandler()
        self.users = []
        self.load_data()
    
    def load_data(self):
        logging.debug("waking up the storage....")
        self.users = self.file_handler.load_data(User, Project, Task)
        if not self.users:
            logging.debug('well ill be damned no users found, initializing empty list')
            self.users = []
        logging.debug(f"loaded{len(self.users)} users")   
    
    def save_data(self):
        logging.debug("Saving data to storage")
        self.file_handler.save_data(self.users)
        logging.debug("my sparrow your data has bee saved")
    
    def find_user_by_name(self, name):
        logging.debug(f"Searching for user by name: '{name}'")
        for user in self.users:
            if user.name.lower() == name.lower():
                logging.debug(f"User found: {user.name} (ID: {user.user_id})")
                return user
        logging.debug(f"User '{name}' not found")
        return None
    
    def find_user_by_id(self, user_id):
        logging.debug(f"Searching for user by ID: '{user_id}'")
        for user in self.users:
            if user.user_id == user_id:
                logging.debug(f"User found: {user.name}")
                return user
        logging.debug(f"User ID '{user_id}' not found")
        return None
    def find_project_by_title(self, user, title):
        logging.debug(f"Searching project '{title}' for user '{user.name}'")
        for project in user.projects:
            if project.title.lower() == title.lower():
                logging.debug(f"Project found: {project.title} (ID: {project.project_id})")
                return project
        logging.debug(f"Project '{title}' not found for user '{user.name}'")
        return None
    def add_user(self, args):
        logging.debug(f"add_user called with name='{args.name}', email='{args.email}'")
        if not validate_email(args.email):
            print("howdy Sparrow! Invalid email format. Email must contain @ and .")
            logging.warning(f"Invalid email format: {args.email}")
            return
        
        existing_ids = [u.user_id for u in self.users if u.user_id]
        user_id = generate_id('USR', existing_ids)
        logging.debug(f"Generated user_id: {user_id}")
        
        user = User(args.name, args.email, user_id)
        self.users.append(user)
        self.save_data()
        print(f"howdy Sparrow! User '{args.name}' added successfully with id: {user_id}")
        logging.info(f"User added: {user.name} ({user.email}) ID: {user_id}")
    
    def list_users(self, args):
        logging.debug("list_users called")
        if not self.users:
            print("howdy Sparrow! No users found.")
            logging.debug("No users to list")
            return
        
        headers = ['ID', 'Name', 'Email', 'Projects Count']
        rows = []
        for user in self.users:
            rows.append([user.user_id, user.name, user.email, len(user.projects)])
        display_table('Users List', headers, rows)
        logging.debug(f"Listed {len(self.users)} users")

    def add_project(self, args):
        logging.debug(f"add_project called: user='{args.user}', title='{args.title}'")
        user = self.find_user_by_name(args.user)
        if not user:
            print(f"howdy Sparrow! User '{args.user}' not found my brother.")
            logging.warning(f"User '{args.user}' not found")
            return
        
        existing_ids = [p.project_id for p in user.projects if p.project_id]
        project_id = generate_id('PRJ', existing_ids)
        logging.debug(f"Generated project_id: {project_id}")
        
        due_date = format_date(args.due_date)
        project = Project(args.title, args.description, due_date, project_id)
        user.add_project(project)
        self.save_data()
        print(f"howdy Sparrow! Project '{args.title}' added to username: '{user.name}' with ID: {project_id}")
        logging.info(f"Project added: {project.title} for user {user.name}")

    def list_projects(self, args):
        logging.debug(f"list_projects called with user filter: {args.user}")
        if args.user:
            user = self.find_user_by_name(args.user)
            if not user:
                print(f"howdy Sparrow! User '{args.user}' not found.")
                return
            
            if not user.projects:
                print(f"howdy Sparrow! User '{user.name}' has no projects.")
                logging.debug(f"No projects for user {user.name}")
                return
            
            headers = ['Project ID', 'Title', 'Description', 'Due Date', 'Tasks']
            rows = []
            for project in user.projects:
                rows.append([project.project_id, project.title, project.description[:30], 
                           project.due_date, len(project.tasks)])
            display_table(f"Projects for {user.name}", headers, rows)
            logging.debug(f"Listed {len(user.projects)} projects for {user.name}")
        else:
            all_projects = []
            for user in self.users:
                for project in user.projects:
                    all_projects.append([user.name, project.project_id, project.title, 
                                       project.due_date, len(project.tasks)])
            
            if not all_projects:
                print("howdy Sparrow! No projects found.")
                logging.debug("No projects exist in the sparow system for project management")
                return
            
            headers = ['User', 'Project ID', 'Title', 'Due Date', 'Tasks']
            display_table('All Projects', headers, all_projects)
            logging.debug(f"Listed {len(all_projects)} projects across all users")

    def search_projects(self, args):
        logging.debug(f"search_projects called: user='{args.user}', term='{args.term}'")
        user = self.find_user_by_name(args.user)
        if not user:
            print(f"howdy Sparrow! User '{args.user}' not found.")
            return
        
        search_term = args.term.lower()
        matching_projects = []
        
        for project in user.projects:
            if search_term in project.title.lower() or search_term in project.description.lower():
                matching_projects.append(project)
                logging.debug(f"Project matches: '{project.title}'")
        
        if not matching_projects:
            print(f"howdy Sparrow! No projects found matching '{args.term}' for user '{user.name}'.")
            logging.debug(f"No matching projects for term '{args.term}'")
            return
        
        headers = ['Project ID', 'Title', 'Description', 'Due Date']
        rows = []
        for project in matching_projects:
            rows.append([project.project_id, project.title, project.description[:30], project.due_date])
        display_table(f"Search Results for '{args.term}'", headers, rows)
        logging.debug(f"Found {len(matching_projects)} matching projects")

    def add_task(self, args):
        logging.debug(f"add_task called: project='{args.project}', title='{args.title}'")
        task_assigned_to = None
        user = None
        
        for u in self.users:
            project = self.find_project_by_title(u, args.project)
            if project:
                user = u
                break
        
        if not user:
            print(f"howdy Sparrow! Project '{args.project}' not found.")
            logging.warning(f"Project '{args.project}' not found in any user")
            return
        
        project = self.find_project_by_title(user, args.project)
        
        existing_ids = [t.task_id for t in project.tasks if t.task_id]
        task_id = generate_id('Task', existing_ids)
        logging.debug(f"Generated task_id: {task_id}")
        
        task = Task(args.title, task_assigned_to, 'pending', task_id)
        project.add_task(task)
        self.save_data()
        print(f"howdy Sparrow! Task '{args.title}' added to project '{project.title}' with ID: {task_id}")
        logging.info(f"Task added: {task.title} to project {project.title}")
    
    def complete_task(self, args):
        logging.debug(f"complete_task called with title='{args.title}'")
        for user in self.users:
            for project in user.projects:
                for task in project.tasks:
                    if task.title.strip().lower() == args.title.strip().lower():
                        logging.debug(f"Found task '{task.title}' in project '{project.title}' for user '{user.name}'")
                        task.mark_complete()
                        self.save_data()
                        print(f"howdy Sparrow! Task '{args.title}' Hereby marked as completed.")
                        logging.info(f"Task completed: {task.title}")
                        return
        logging.warning(f"Task '{args.title}' not found in any project")
        print(f"howdy Sparrow! Task '{args.title}' not found.")
    
    def list_tasks(self, args):
        logging.debug(f"list_tasks called: user='{args.user}', project='{args.project}'")
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
            logging.debug(f"No tasks in project {project.title}")
            return
        
        headers = ['Task ID', 'Title', 'Status Project']
        rows = []
        for task in project.tasks:
            rows.append([task.task_id, task.title, task.status])
        display_table(f"Tasks for {project.title}", headers, rows)
        logging.debug(f"Listed {len(project.tasks)} tasks for project {project.title}")
        
    def delete_user(self, args):
        logging.debug(f"delete_user called: name='{args.name}'")
        user = self.find_user_by_name(args.name)
        if not user:
            print(f"howdy Sparrow! User '{args.name}' not found.")
            return
        
        self.users.remove(user)
        self.save_data()
        print(f"howdy Sparrow! User '{args.name}' deleted successfully.")
        logging.info(f"User deleted: {user.name} (ID: {user.user_id})")

def main():
    logging.debug("howdy we starting CLI application")
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

    delete_parser = subparsers.add_parser('delete-user', help='Delete a user')
    delete_parser.add_argument('--name', required=True, help='User name')
    
    args = parser.parse_args()
    logging.debug(f"Command received: {args.command if args.command else 'None'}")
    
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
    elif args.command == 'delete-user':
        cli.delete_user(args) 
    else:
        parser.print_help()
        logging.warning("No valid command provided")
        
if __name__ == '__main__':
    main()