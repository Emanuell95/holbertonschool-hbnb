from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship, validates
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Review(Base):
    """Review model for storing review details."""
    __tablename__ = 'reviews'

    id = Column(Integer, primary_key=True, autoincrement=True)  # ✅ Integer (Auto-Incremented)
    text = Column(String, nullable=False)
    rating = Column(Integer, nullable=False)
    place_id = Column(Integer, ForeignKey('places.id'), nullable=False)  # ✅ One-to-Many (Place → Review)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)  # ✅ One-to-Many (User → Review)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 🟢 Relationships
    place = relationship("Place", back_populates="reviews", lazy="joined")  # ✅ One-to-Many (Place → Review)
    user = relationship("User", back_populates="reviews", lazy="joined")  # ✅ One-to-Many (User → Review)

    def __init__(self, text, rating, place_id, user_id):
        self.text = text
        self.rating = rating
        self.place_id = place_id  # Store only the Place ID
        self.user_id = user_id  # Store only the User ID

    @validates("text")
    def validate_text(self, key, value):
        """Ensure the review text is not empty."""
        if not value or value.strip() == "":
            raise ValueError("Review text cannot be empty.")
        return value

    @validates("rating")
    def validate_rating(self, key, value):
        """Ensure the rating is between 1 and 5."""
        if not isinstance(value, int) or not (1 <= value <= 5):
            raise ValueError("Rating must be between 1 and 5.")
        return value

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