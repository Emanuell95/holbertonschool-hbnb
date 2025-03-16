from werkzeug.security import generate_password_hash

def hash_password(password: str) -> str:
    """Hashes a password using a secure hashing algorithm."""
    return generate_password_hash(password)