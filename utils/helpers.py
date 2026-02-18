"""
Utility helper functions
"""
import random
import string
from datetime import datetime, timedelta


def generate_random_string(length=8):
    """Generate random alphanumeric string"""
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))


def format_currency(amount):
    """Format amount as currency"""
    return f"₹{amount:,.2f}"


def calculate_percentage(part, whole):
    """Calculate percentage"""
    if whole == 0:
        return 0
    return (part / whole) * 100


def get_date_range(days=30):
    """Get date range for last N days"""
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    return start_date, end_date


def truncate_text(text, max_length=50):
    """Truncate text to max length"""
    if len(text) <= max_length:
        return text
    return text[:max_length-3] + "..."


def validate_email(email):
    """Basic email validation"""
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def validate_phone(phone):
    """Basic phone validation"""
    import re
    # Remove spaces and special characters
    cleaned = re.sub(r'[^\d+]', '', phone)
    return len(cleaned) >= 10
