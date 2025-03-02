from datetime import datetime
import uuid
from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import validates

Base = declarative_base()

class Amenity(Base):
    """Amenity model for storing amenity details."""
    __tablename__ = 'amenities'

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(50), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __init__(self, name):
        self.name = self.validate_name(name)

    @validates("name")
    def validate_name(self, key, value):
        if not value or value.strip() == "":
            raise ValueError("Amenity name cannot be empty")
        return value

    @staticmethod
    def validate_name(name: str) -> str:
        """Ensures the name is within the allowed length."""
        if not name or len(name) > 50:
            raise ValueError("Amenity name must be between 1 and 50 characters.")
        return name

    def to_dict(self) -> dict:
        """Converts the amenity object to a dictionary."""
        return {
            "id": self.id,
            "name": self.name,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

    def __repr__(self) -> str:
        return f"<Amenity {self.name}>"
