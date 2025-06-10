from werkzeug.security import generate_password_hash, check_password_hash
import re

def hash_password(password: str) -> str:
    return generate_password_hash(password)

def verify_password(stored_password: str, provided_password: str) -> bool:
    return check_password_hash(stored_password, provided_password)

def is_valid_email(email: str) -> bool:
    regex = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return re.match(regex, email) is not None

def is_valid_password(password: str) -> bool:
    return len(password) >= 8 and any(c.isdigit() for c in password) and any(c.isalpha() for c in password)