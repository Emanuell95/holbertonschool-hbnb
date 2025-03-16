import uuid
import re
from datetime import datetime
from sqlalchemy import Column, String, Boolean, DateTime
from sqlalchemy.orm import relationship, validates
from flask_bcrypt import Bcrypt
from app import db
import os

bcrypt = Bcrypt()

class User(db.Model):  # Ensure this extends db.Model for SQLAlchemy
    """User model for storing user details."""
    __tablename__ = 'users'

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    first_name = Column(String(255), nullable=False)
    last_name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    places = relationship("Place", back_populates="owner", cascade="all, delete")  
    reviews = relationship("Review", back_populates="user", cascade="all, delete")  

    def __init__(self, first_name, last_name, email, password, is_admin=False):
        self.first_name = self.validate_name(first_name, "First name")
        self.last_name = self.validate_name(last_name, "Last name")
        self.email = self.validate_email(email)
        self.password = self.hash_password(password)
        self.is_admin = is_admin

    def hash_password(self, password):
        """Hashes the password before storing it."""
        return bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
        """Verifies if the provided password matches the hashed password."""
        return bcrypt.check_password_hash(self.password, password)

    @staticmethod
    def validate_name(name: str, field: str) -> str:
        """Ensures the name is within the allowed length."""
        if not name or len(name.strip()) == 0 or len(name) > 255:
            raise ValueError(f"{field} must be between 1 and 255 characters.")
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

# Function to execute schema.sql when initializing the database
def execute_sql_file(sql_file_path):
    """Executes a raw SQL file in MySQL."""
    with open(sql_file_path, "r") as file:
        sql_commands = file.read()
    db.session.execute(sql_commands)
    db.session.commit()

# Check if script should execute raw SQL
schema_path = os.path.join(os.path.dirname(__file__), "schema.sql")

if os.path.exists(schema_path):
    execute_sql_file(schema_path)
    print("Database schema.sql executed successfully!")
else:
    print("schema.sql not found, skipping raw SQL execution.")