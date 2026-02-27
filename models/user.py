import hashlib
import uuid
from models.person import Person

class User(Person):
    """User class with authentication and role-based access"""
    
    _id_counter = 1000  # Class attribute for ID generation
    
    def __init__(self, name, email, password, role='user'):
        super().__init__(name, email)
        self._user_id = f"U{User._id_counter}"
        User._id_counter += 1
        self._password_hash = self._hash_password(password)
        self._role = role  # 'admin' or 'user'
        self._projects = []  # List of project IDs
    
    def _hash_password(self, password):
        """Hash password for secure storage"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def verify_password(self, password):
        """Verify provided password"""
        return self._password_hash == hashlib.sha256(password.encode()).hexdigest()
    
    @property
    def user_id(self):
        return self._user_id
    
    @property
    def role(self):
        return self._role
    
    @role.setter
    def role(self, value):
        if value not in ['admin', 'user']:
            raise ValueError("Role must be 'admin' or 'user'")
        self._role = value
    
    def get_role(self):
        return self.role
    
    def add_project(self, project_id):
        if project_id not in self._projects:
            self._projects.append(project_id)
    
    def to_dict(self):
        """Convert user to dictionary for JSON storage"""
        return {
            'user_id': self._user_id,
            'name': self._name,
            'email': self._email,
            'password_hash': self._password_hash,
            'role': self._role,
            'projects': self._projects
        }
    
    @classmethod
    def from_dict(cls, data):
        """Create user from dictionary"""
        user = cls(data['name'], data['email'], 'temp', data['role'])
        user._user_id = data['user_id']
        user._password_hash = data['password_hash']
        user._projects = data.get('projects', [])
        return user
    
    def __str__(self):
        return f"[{self.user_id}] {self.name} ({self.role})"