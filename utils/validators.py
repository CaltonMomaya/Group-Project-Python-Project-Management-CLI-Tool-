import re
from datetime import datetime

def validate_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_date(date_str):
    """Validate date format (YYYY-MM-DD)"""
    try:
        datetime.strptime(date_str, '%Y-%m-%d')
        return True
    except ValueError:
        return False

def validate_non_empty(value, field_name):
    """Validate that a value is not empty"""
    if not value or len(value.strip()) == 0:
        raise ValueError(f"{field_name} cannot be empty")
    return value.strip()

def validate_choice(value, choices, field_name):
    """Validate that a value is in allowed choices"""
    if value not in choices:
        raise ValueError(f"{field_name} must be one of: {', '.join(choices)}")
    return value