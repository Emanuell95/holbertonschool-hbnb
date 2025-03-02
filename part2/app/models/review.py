from datetime import datetime
import uuid
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.orm import validates

Base = declarative_base()

class Review(Base):
    """Review model for storing review details."""
    __tablename__ = 'reviews'

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    text = Column(String, nullable=False)
    rating = Column(Integer, nullable=False)
    place_id = Column(String(36), ForeignKey('places.id'), nullable=False)
    user_id = Column(String(36), ForeignKey('users.id'), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    place = relationship('Place')
    user = relationship('User')

    @validates("text")
    def validate_text(self, key, value):
        if not value or value.strip() == "":
            raise ValueError("Review text cannot be empty")
        return value

    @validates("user_id", "place_id")
    def validate_foreign_keys(self, key, value):
        if not value:
            raise ValueError(f"{key} must be a valid reference")
        return value

    def __init__(self, text, rating, place, user):
        self.text = self.validate_text(text)
        self.rating = self.validate_rating(rating)
        self.place = place
        self.user = user

    @staticmethod
    def validate_text(text: str) -> str:
        """Ensures the review text is provided."""
        if not text:
            raise ValueError("Review text cannot be empty.")
        return text

    @staticmethod
    def validate_rating(rating: int) -> int:
        """Ensures the rating is between 1 and 5."""
        if rating < 1 or rating > 5:
            raise ValueError("Rating must be between 1 and 5.")
        return rating

    def to_dict(self) -> dict:
        """Converts the review object to a dictionary."""
        return {
            "id": self.id,
            "text": self.text,
            "rating": self.rating,
            "place_id": self.place_id,
            "user_id": self.user_id,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

    def __repr__(self) -> str:
        return f"<Review {self.text[:30]} (Rating: {self.rating})>"
