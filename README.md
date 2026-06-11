# Project Management CLI Tool

<p align="center">
  <img src="https://readme-typing-svg.demolab.com?font=JetBrains+Mono&weight=600&size=28&pause=1200&color=36BCF7&center=true&vCenter=true&width=1000&lines=Howdy+Esteemed+Viewer+Welcome+to+the+Project+Documentation;A+Step-by-Step+Guide;Built+with+Python" alt="Typing SVG" />
</p>

## Setup Instructions

1. **Clone the repository**  
   `git clone "your repository link`
2. **instal pipenv**
   `pip install pipenv`
3. **install production dependencies
   `pipenv install python-dateutil prettytable`

3. **Install dev dependencies with Pipenv**  
   `pipenv install --dev pytest`

4. **Activate the virtual environment**  
   `pipenv shell` (no python -m venv .venv)

5. **Run the CLI tool**  
   `python main.py --help`


## Disclaimer

The CLI commands below are examples – replace `"Sparrowlen"` with your own user name. Have fun, fellow Sparrow Viewer!. be sure also to add spaces

## How to Run CLI Commands

General syntax:  
`python main.py (your commands based on the following be sure to strictyly adhere to it)`

### 1. Add a user
`python main.py add-user --name "Sparrowlen" --email "sparrowlen@example.com"`

### 2. Add another user
`python main.py add-user --name "Sparrowlen2" --email "sparrowlen2@example.com"`

### 3. List all users
`python main.py list-users`

### 4. Add a project for Sparrowlen
`python main.py add-project --user "Sparrowlen" --title "e-commerce Website" --description "Build a fully functional e-commerce platform" --due-date "2025-12-31"`

### 5. Add another project for Sparrowlen
`python main.py add-project --user "Sparrowlen" --title "Mobile App" --description "Develop iOS and Android app (Flutter & Dart)" --due-date "2025-03-15"`

### 6. Add project for Sparrowlen2
`python main.py add-project --user "Sparrowlen2" --title "Database Migration" --description "Migrate legacy database to cloud" --due-date "2025-10-30"`

### 7. List all projects
`python main.py list-projects`

### 8. List projects for specific user
`python main.py list-projects --user "Sparrowlen"`

### 9. Add tasks to a project
`python main.py add-task --project "e-commerce Website" --title "Design database schema"`

### 10. Add more tasks
`python main.py add-task --project "e-commerce Website" --title "Implement user authentication"`  
`python main.py add-task --project "e-commerce Website" --title "Create shopping cart feature"`

### 11. List tasks for a project
`python main.py list-tasks --user "Sparrowlen" --project "e-commerce Website"`

### 12. Complete a task
`python main.py complete-task --title "Design database schema"`

### 13. View tasks again to see status change
`python main.py list-tasks --user "Sparrowlen" --project "e-commerce Website"`

### 14. Search projects
`python main.py search-projects --user "Sparrowlen2" --term "website"`

### 15. Delete a user
`python main.py delete-user --name "Sparrowlen2"`

### 16. Verify user was deleted
`python main.py list-users`

## Available Commands (Summary)

### User Management
- `add-user --name "NAME" --email "EMAIL"`
- `list-users`
- `delete-user --name "NAME"`

### Project Management
- `add-project --user "USER" --title "TITLE" --description "DESC" --due-date "YYYY-MM-DD"`
- `list-projects` (or `--user "USER"`)
- `search-projects --user "USER" --term "KEYWORD"`

### Task Management
- `add-task --project "PROJECT_TITLE" --title "TASK_TITLE"`
- `list-tasks --user "USER" --project "PROJECT_TITLE"`
- `complete-task --title "TASK_TITLE"`

## Features

- **User management** – create, list, delete users with unique IDs (e.g., USR1, USR2)
- **Project management** – add projects to specific users with due dates
- **Task management** – assign tasks to projects, mark them as complete
- **Search** – find projects by title or description for a given user
- **Persistent storage** – all data saved in `data/storage.json` (JSON format)
- **Pretty table output** – uses `prettytable` for clean terminal display
- **Flexible date parsing** – via `python-dateutil` (accepts many formats)
- **Debug logging** – built‑in `logging` module shows timestamps, levels (DEBUG, INFO, WARNING)
- **Object‑oriented design** – inheritance (`BaseEntity`), `@property` setters, class‑based ID counters, `__str__` / `__repr__`

## Project Structure

```text
project-management-cli/
├── main.py                     # CLI entry point (argparse + logging)
├── models/
│   ├── base.py                 # BaseEntity class (inheritance, __str__, __repr__)
│   ├── user.py                 # User model (email property, class ID counter)
│   ├── project.py              # Project model (task container, to/from dict)
│   └── task.py                 # Task model (status property, mark_complete)
├── utils/
│   ├── file_handler.py         # JSON persistence (save/load with error handling)
│   └── helpers.py              # validate_email, format_date, display_table, generate_id
├── data/
│   └── storage.json            # Auto-created JSON data file when users perform specific actions
├── tests/
│   ├── test_user.py
│   ├── test_project.py
│   ├── test_task.py
│   └── test_file_handler.py
├── Pipfile                     # Dependencies (contains production & development packages)
├── Pipfile.lock
└── README.md
```

## GIT WORKFLOW

### This project follows a professional branching model:

1. main – stable release branch (merged from dev after full testing)

2. dev – integration branch for all feature development

### Feature branches (each created from dev, merged via Pull Request):

3. feature/cli-add-user – user commands

4. feature/cli-projects – project commands

5. feature/cli-tasks – task commands

6. feature/cli-delete-user – delete user command

7. feature/tests – unit tests

8. feature/logging – debug logging

## Dependencies
 `python-dateutil` Flexible date parsing (e.g., "tomorrow", "2025-12-31)
 `prettytable` Formatted ASCII tables in terminal 
 `pytest` Test runner

All dependencies are managed with `pipenv`.  
Install them using:

1. pipenv install --dev   

## testing
1. pipenv install pytest --dev
2. pipenv run pytest
3. pipenv run pytest tests/test_task.py (to run a single test)
4. (use unittest alternatvely)python -m unittest tests.test_user.py (since iko kwa the tests folder)

## Troubleshooting
1. "Module not found" – Run pipenv install first, then use pipenv shell or pipenv run.
2. Task not found when marking complete – Ensure the exact title (case‑insensitive) and that the task exists in a project. Use list-tasks to verify.
3. nvalid email – Email must contain @ and ..

## Limitations
1. The prettytable output may wrap or cut long descriptions (truncated to 30 characters).
2. No authentication or multi‑admin support – it is a single‑user simulation.

## Acknowledgements
1. Python Software Foundation
2. Contributors to python-dateutil and prettytable
3. Course instructor for OOP and CLI guidance

## AUTHOR
Sparrowlen
GitHub:https://github.com/Sparrowlen1
Email: dannymuthui118@gmail.com
