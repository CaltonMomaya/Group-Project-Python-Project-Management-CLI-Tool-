from abc import ABC, abstractmethod

class Person(ABC):
    """Base class for all persons in the system"""
    
    def __init__(self, name, email):
        self._name = name
        self._email = email
    
    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, value):
        if not value or len(value.strip()) == 0:
            raise ValueError("Name cannot be empty")
        self._name = value.strip()
    
    @property
    def email(self):
        return self._email
    
    @email.setter
    def email(self, value):
        if '@' not in value:
            raise ValueError("Invalid email format")
        self._email = value
    
    @abstractmethod
    def get_role(self):
        """Abstract method to be implemented by subclasses"""
        pass
    
    def __str__(self):
        return f"{self.name} ({self.email})"