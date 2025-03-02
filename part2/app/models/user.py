from datetime import datetime
import uuid
import re
from sqlalchemy import Column, String, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import validates

Base = declarative_base()

class User(Base):
    """User model for storing user details."""
    __tablename__ = 'users'

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    @validates("first_name", "last_name")
    def validate_name(self, key, value):
        if not value or value.strip() == "":
            raise ValueError(f"{key} cannot be empty")
        return value

    @validates("email")
    def validate_email(self, key, value):
        if not re.match(r"[^@]+@[^@]+\.[^@]+", value):
            raise ValueError("Invalid email format")
        return value

    def __init__(self, first_name, last_name, email, is_admin=False):
        self.first_name = self.validate_name(first_name, "First name")
        self.last_name = self.validate_name(last_name, "Last name")
        self.email = self.validate_email(email)
        self.is_admin = is_admin

    @staticmethod
    def validate_name(name: str, field: str) -> str:
        """Ensures the name is within the allowed length."""
        if not name or len(name) > 50:
            raise ValueError(f"{field} must be between 1 and 50 characters.")
        return name

    @staticmethod
    def validate_email(email: str) -> str:
        """Validates email format."""
        email_regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if not re.match(email_regex, email):
            raise ValueError("Invalid email format.")
        return email

    def to_dict(self) -> dict:
        """Converts the user object to a dictionary."""
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "is_admin": self.is_admin,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

    def __repr__(self) -> str:
        return f"<User {self.first_name} {self.last_name} ({self.email})>"
