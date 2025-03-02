from datetime import datetime
import uuid
from sqlalchemy import Column, String, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship, validates
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Place(Base):
    """Place model for storing place details."""
    __tablename__ = 'places'

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String(100), nullable=False)
    description = Column(String, nullable=True)
    price = Column(Float, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    owner_id = Column(String(36), ForeignKey('users.id'), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    owner = relationship('User', foreign_keys=[owner_id])

    def __init__(self, title, description, price, latitude, longitude, owner):
        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner_id = owner.id  # Assign only the owner's ID

    @validates('title')
    def validate_title(self, key, title):
        """Ensures the title is within the allowed length."""
        if not title or len(title) > 100:
            raise ValueError("Title must be between 1 and 100 characters.")
        return title

    @validates('price')
    def validate_price(self, key, price):
        """Ensures the price is positive."""
        if price < 0:
            raise ValueError("Price must be a positive value.")
        return price

    @validates('latitude')
    def validate_latitude(self, key, latitude):
        """Ensures latitude is within -90 to 90."""
        if latitude < -90.0 or latitude > 90.0:
            raise ValueError("Latitude must be between -90.0 and 90.0.")
        return latitude

    @validates('longitude')
    def validate_longitude(self, key, longitude):
        """Ensures longitude is within -180 to 180."""
        if longitude < -180.0 or longitude > 180.0:
            raise ValueError("Longitude must be between -180.0 and 180.0.")
        return longitude

    def to_dict(self) -> dict:
        """Converts the place object to a dictionary."""
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "price": self.price,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "owner_id": self.owner_id,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

    def __repr__(self) -> str:
        return f"<Place {self.title} ({self.price})>"