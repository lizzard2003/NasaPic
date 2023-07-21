# this is used to validate the user input 
import re



def validate_registration(username, email, password):
    errors = []

    # Required fields check
    if not username:
        errors.append("Username is required.")
    if not email:
        errors.append("Email address is required.")
    if not password:
        errors.append("Password is required.")

    # Email validation
    if email and not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        errors.append("Invalid email address.")

    # Password complexity check
    if password and len(password) < 8:
        errors.append("Password must be at least 8 characters long.")
    if password and not re.search(r"[A-Z]", password):
        errors.append("Password must contain an uppercase letter.")
    if password and not re.search(r"[a-z]", password):
        errors.append("Password must contain a lowercase letter.")
    if password and not re.search(r"\d", password):
        errors.append("Password must contain a digit.")

    return errors

