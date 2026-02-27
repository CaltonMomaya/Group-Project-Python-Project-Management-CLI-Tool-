class Task:
    """Task class representing tasks within projects"""
    
    _id_counter = 1
    
    def __init__(self, title, project_id, assigned_to=None):
        self._task_id = f"T{Task._id_counter}"
        Task._id_counter += 1
        self._title = title
        self._project_id = project_id
        self._assigned_to = assigned_to
        self._status = 'pending'  # pending, in_progress, completed
        self._created_at = datetime.now().isoformat()
    
    @property
    def task_id(self):
        return self._task_id
    
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
        if value not in ['pending', 'in_progress', 'completed']:
            raise ValueError("Invalid status")
        self._status = value
    
    def to_dict(self):
        return {
            'task_id': self._task_id,
            'title': self._title,
            'project_id': self._project_id,
            'assigned_to': self._assigned_to,
            'status': self._status,
            'created_at': self._created_at
        }
    
    @classmethod
    def from_dict(cls, data):
        task = cls(data['title'], data['project_id'], data.get('assigned_to'))
        task._task_id = data['task_id']
        task._status = data.get('status', 'pending')
        task._created_at = data.get('created_at', datetime.now().isoformat())
        return task
    
    def __str__(self):
        assigned = self._assigned_to if self._assigned_to else "Unassigned"
        return f"[{self.task_id}] {self.title} - {self.status} (Assigned to: {assigned})"