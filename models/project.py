from datetime import datetime

class Project:
    """Project class representing a project in the system"""
    
    _id_counter = 1
    
    def __init__(self, title, description, due_date, owner_id):
        self._project_id = f"P{Project._id_counter}"
        Project._id_counter += 1
        self._title = title
        self._description = description
        self._due_date = due_date
        self._owner_id = owner_id
        self._tasks = []  # List of task IDs
        self._created_at = datetime.now().isoformat()
        self._status = 'active'  # active, completed, archived
    
    @property
    def project_id(self):
        return self._project_id
    
    @property
    def title(self):
        return self._title
    
    @title.setter
    def title(self, value):
        if not value or len(value.strip()) == 0:
            raise ValueError("Title cannot be empty")
        self._title = value.strip()
    
    @property
    def status(self):
        return self._status
    
    @status.setter
    def status(self, value):
        if value not in ['active', 'completed', 'archived']:
            raise ValueError("Invalid status")
        self._status = value
    
    def add_task(self, task_id):
        if task_id not in self._tasks:
            self._tasks.append(task_id)
    
    def to_dict(self):
        return {
            'project_id': self._project_id,
            'title': self._title,
            'description': self._description,
            'due_date': self._due_date,
            'owner_id': self._owner_id,
            'tasks': self._tasks,
            'created_at': self._created_at,
            'status': self._status
        }
    
    @classmethod
    def from_dict(cls, data):
        project = cls(
            data['title'], 
            data['description'], 
            data['due_date'], 
            data['owner_id']
        )
        project._project_id = data['project_id']
        project._tasks = data.get('tasks', [])
        project._created_at = data.get('created_at', datetime.now().isoformat())
        project._status = data.get('status', 'active')
        return project
    
    def __str__(self):
        return f"[{self.project_id}] {self.title} - {self.status}"