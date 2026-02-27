#!/usr/bin/env python3
"""
Project Management CLI Tool
A command-line interface for managing projects and tasks
"""

import argparse
import sys
from models.user import User
from models.project import Project
from models.task import Task
from utils.storage import JSONStorage
from utils.auth import login_required, admin_required, log_action
from utils.validators import validate_email, validate_date
import getpass
from tabulate import tabulate  # External package

class ProjectManagementCLI:
    """Main CLI application class"""
    
    def __init__(self):
        self.current_user = None
        self.user_storage = JSONStorage('data/users.json')
        self.project_storage = JSONStorage('data/projects.json')
        self.task_storage = JSONStorage('data/tasks.json')
        self.load_data()
    
    def load_data(self):
        """Load all data from JSON files"""
        # Load users
        user_data = self.user_storage.load()
        self.users = {u['user_id']: User.from_dict(u) for u in user_data}
        
        # Load projects
        project_data = self.project_storage.load()
        self.projects = {p['project_id']: Project.from_dict(p) for p in project_data}
        
        # Load tasks
        task_data = self.task_storage.load()
        self.tasks = {t['task_id']: Task.from_dict(t) for t in task_data}
    
    def save_all(self):
        """Save all data to JSON files"""
        self.user_storage.save([u.to_dict() for u in self.users.values()])
        self.project_storage.save([p.to_dict() for p in self.projects.values()])
        self.task_storage.save([t.to_dict() for t in self.tasks.values()])
    
    def register_user(self, args):
        """Register a new user"""
        print("\n📝 User Registration")
        name = input("Name: ").strip()
        email = input("Email: ").strip()
        
        if not validate_email(email):
            print("❌ Invalid email format")
            return
        
        # Check if email already exists
        if any(u.email == email for u in self.users.values()):
            print("❌ Email already registered")
            return
        
        password = getpass.getpass("Password: ")
        confirm = getpass.getpass("Confirm password: ")
        
        if password != confirm:
            print("❌ Passwords do not match")
            return
        
        role = 'admin' if len(self.users) == 0 else 'user'  # First user is admin
        
        user = User(name, email, password, role)
        self.users[user.user_id] = user
        self.save_all()
        
        print(f"✅ User registered successfully! Your ID: {user.user_id}")
        print(f"Role: {role}")
    
    def login(self, args):
        """Login user"""
        print("\n🔐 Login")
        email = input("Email: ").strip()
        password = getpass.getpass("Password: ")
        
        # Find user by email
        user = next((u for u in self.users.values() if u.email == email), None)
        
        if user and user.verify_password(password):
            self.current_user = user
            print(f"✅ Welcome back, {user.name}! (Role: {user.role})")
        else:
            print("❌ Invalid email or password")
    
    def logout(self, args):
        """Logout current user"""
        if self.current_user:
            print(f"👋 Goodbye, {self.current_user.name}!")
            self.current_user = None
        else:
            print("You are not logged in")
    
    @login_required
    def create_project(self, args):
        """Create a new project"""
        print("\n📁 Create New Project")
        title = input("Project title: ").strip()
        if not title:
            print("❌ Title cannot be empty")
            return
        
        description = input("Description: ").strip()
        due_date = input("Due date (YYYY-MM-DD): ").strip()
        
        if not validate_date(due_date):
            print("❌ Invalid date format. Use YYYY-MM-DD")
            return
        
        project = Project(title, description, due_date, self.current_user.user_id)
        self.projects[project.project_id] = project
        self.current_user.add_project(project.project_id)
        self.save_all()
        
        print(f"✅ Project created successfully! ID: {project.project_id}")
    
    @login_required
    def list_projects(self, args):
        """List all projects"""
        if not self.projects:
            print("No projects found")
            return
        
        # Filter projects based on user role
        if self.current_user.role == 'admin':
            projects_list = self.projects.values()
        else:
            projects_list = [p for p in self.projects.values() 
                           if p._owner_id == self.current_user.user_id]
        
        if not projects_list:
            print("No projects found")
            return
        
        table_data = []
        for p in projects_list:
            owner = self.users.get(p._owner_id, None)
            owner_name = owner.name if owner else "Unknown"
            table_data.append([
                p.project_id,
                p.title,
                p.status,
                p.due_date,
                owner_name,
                len(p._tasks)
            ])
        
        headers = ["ID", "Title", "Status", "Due Date", "Owner", "Tasks"]
        print("\n" + tabulate(table_data, headers=headers, tablefmt="grid"))
    
    @login_required
    def create_task(self, args):
        """Create a new task"""
        print("\n📋 Create New Task")
        
        # Show available projects
        self.list_projects(args)
        
        project_id = input("Project ID: ").strip()
        if project_id not in self.projects:
            print("❌ Project not found")
            return
        
        project = self.projects[project_id]
        
        # Check permission
        if self.current_user.role != 'admin' and project._owner_id != self.current_user.user_id:
            print("❌ You don't have permission to add tasks to this project")
            return
        
        title = input("Task title: ").strip()
        if not title:
            print("❌ Title cannot be empty")
            return
        
        # Show available users for assignment
        print("\nAvailable users:")
        for uid, user in self.users.items():
            print(f"  {uid}: {user.name}")
        
        assigned_to = input("Assign to (user ID, optional): ").strip() or None
        if assigned_to and assigned_to not in self.users:
            print("❌ User not found")
            return
        
        task = Task(title, project_id, assigned_to)
        self.tasks[task.task_id] = task
        project.add_task(task.task_id)
        self.save_all()
        
        print(f"✅ Task created successfully! ID: {task.task_id}")
    
    @login_required
    def list_tasks(self, args):
        """List tasks with optional filtering"""
        filter_by = input("Filter by (all/project/user): ").lower().strip()
        
        tasks_list = []
        if filter_by == 'project':
            project_id = input("Project ID: ").strip()
            if project_id in self.projects:
                tasks_list = [t for t in self.tasks.values() 
                            if t._project_id == project_id]
        elif filter_by == 'user':
            user_id = input("User ID: ").strip()
            if user_id in self.users:
                tasks_list = [t for t in self.tasks.values() 
                            if t._assigned_to == user_id]
        else:
            tasks_list = list(self.tasks.values())
        
        if not tasks_list:
            print("No tasks found")
            return
        
        table_data = []
        for t in tasks_list:
            project = self.projects.get(t._project_id)
            project_title = project.title if project else "Unknown"
            assigned = self.users.get(t._assigned_to, None)
            assigned_name = assigned.name if assigned else "Unassigned"
            table_data.append([
                t.task_id,
                t.title,
                t.status,
                project_title,
                assigned_name
            ])
        
        headers = ["ID", "Title", "Status", "Project", "Assigned To"]
        print("\n" + tabulate(table_data, headers=headers, tablefmt="grid"))
    
    @login_required
    @log_action
    def update_task_status(self, args):
        """Update task status"""
        task_id = input("Task ID: ").strip()
        if task_id not in self.tasks:
            print("❌ Task not found")
            return
        
        task = self.tasks[task_id]
        
        # Check permission
        project = self.projects.get(task._project_id)
        if (self.current_user.role != 'admin' and 
            project._owner_id != self.current_user.user_id and
            task._assigned_to != self.current_user.user_id):
            print("❌ You don't have permission to update this task")
            return
        
        print(f"Current status: {task.status}")
        print("Available statuses: pending, in_progress, completed")
        new_status = input("New status: ").strip().lower()
        
        if new_status not in ['pending', 'in_progress', 'completed']:
            print("❌ Invalid status")
            return
        
        task.status = new_status
        self.save_all()
        print(f"✅ Task status updated to: {new_status}")
    
    @admin_required
    def list_users(self, args):
        """List all users (admin only)"""
        if not self.users:
            print("No users found")
            return
        
        table_data = []
        for u in self.users.values():
            table_data.append([
                u.user_id,
                u.name,
                u.email,
                u.role,
                len(u._projects)
            ])
        
        headers = ["ID", "Name", "Email", "Role", "Projects"]
        print("\n" + tabulate(table_data, headers=headers, tablefmt="grid"))
    
    @admin_required
    def change_user_role(self, args):
        """Change user role (admin only)"""
        user_id = input("User ID: ").strip()
        if user_id not in self.users:
            print("❌ User not found")
            return
        
        user = self.users[user_id]
        print(f"Current role: {user.role}")
        new_role = input("New role (admin/user): ").strip().lower()
        
        if new_role not in ['admin', 'user']:
            print("❌ Invalid role")
            return
        
        user.role = new_role
        self.save_all()
        print(f"✅ User role updated to: {new_role}")
    
    def show_menu(self):
        """Display main menu"""
        print("\n" + "="*50)
        print("📊 PROJECT MANAGEMENT CLI")
        print("="*50)
        
        if self.current_user:
            print(f"Logged in as: {self.current_user.name} ({self.current_user.role})")
            print("\nCommands:")
            print("  projects list              - List all projects")
            print("  projects create            - Create new project")
            print("  tasks list                 - List tasks")
            print("  tasks create               - Create new task")
            print("  tasks update                - Update task status")
            
            if self.current_user.role == 'admin':
                print("  users list                 - List all users")
                print("  users role                  - Change user role")
            
            print("  logout                     - Logout")
        else:
            print("\nCommands:")
            print("  register                   - Register new user")
            print("  login                      - Login")
        
        print("  help                       - Show this menu")
        print("  exit                       - Exit application")
        print("="*50)
    
    def run(self):
        """Main CLI loop"""
        print("🚀 Welcome to Project Management CLI!")
        print("Type 'help' to see available commands, 'exit' to quit")
        
        while True:
            try:
                if self.current_user:
                    prompt = f"\n[{self.current_user.name}] $ "
                else:
                    prompt = "\n[guest] $ "
                
                command = input(prompt).strip().lower()
                
                if not command:
                    continue
                
                if command == 'exit':
                    print("👋 Goodbye!")
                    break
                elif command == 'help':
                    self.show_menu()
                elif command == 'register':
                    self.register_user(None)
                elif command == 'login':
                    self.login(None)
                elif command == 'logout':
                    self.logout(None)
                elif command == 'projects list':
                    self.list_projects(None)
                elif command == 'projects create':
                    self.create_project(None)
                elif command == 'tasks list':
                    self.list_tasks(None)
                elif command == 'tasks create':
                    self.create_task(None)
                elif command == 'tasks update':
                    self.update_task_status(None)
                elif command == 'users list' and self.current_user and self.current_user.role == 'admin':
                    self.list_users(None)
                elif command == 'users role' and self.current_user and self.current_user.role == 'admin':
                    self.change_user_role(None)
                else:
                    print("❌ Unknown command. Type 'help' for available commands.")
            
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"❌ Error: {e}")

def main():
    parser = argparse.ArgumentParser(description='Project Management CLI Tool')
    parser.add_argument('--version', action='version', version='PM CLI 1.0.0')
    
    args = parser.parse_args()
    
    app = ProjectManagementCLI()
    app.run()

if __name__ == "__main__":
    main()