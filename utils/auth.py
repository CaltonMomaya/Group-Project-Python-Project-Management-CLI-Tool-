from functools import wraps
import getpass

def login_required(func):
    """Decorator to check if user is logged in"""
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        if not self.current_user:
            print("❌ You must be logged in to perform this action.")
            return None
        return func(self, *args, **kwargs)
    return wrapper

def admin_required(func):
    """Decorator to check if user has admin role"""
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        if not self.current_user:
            print("❌ You must be logged in to perform this action.")
            return None
        if self.current_user.role != 'admin':
            print("❌ Admin access required for this action.")
            return None
        return func(self, *args, **kwargs)
    return wrapper

def log_action(func):
    """Decorator to log user actions"""
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        result = func(self, *args, **kwargs)
        if self.current_user:
            print(f"📝 Action logged: {func.__name__} by {self.current_user.name}")
        return result
    return wrapper