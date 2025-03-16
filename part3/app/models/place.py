from datetime import datetime
import uuid
from sqlalchemy import Column, String, DateTime, Float, Integer, ForeignKey, Table
from sqlalchemy.orm import relationship, validates
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# 🟢 Many-to-Many Association Table (Place ↔ Amenity)
place_amenity_association = Table(
    "place_amenity",
    Base.metadata,
    Column("place_id", String(36), ForeignKey("places.id"), primary_key=True),
    Column("amenity_id", String(36), ForeignKey("amenities.id"), primary_key=True)
)

class Place(Base):
    """Place model for storing place details."""
    __tablename__ = 'places'

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String(100), nullable=False)
    description = Column(String, nullable=True)
    price = Column(Float, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    owner_id = Column(String(36), ForeignKey("users.id"), nullable=False)  # 🟢 One-to-Many (User → Place)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    owner = relationship("User", back_populates="places")  # 🟢 One-to-Many (User → Place)
    reviews = relationship("Review", back_populates="place", cascade="all, delete")  # 🟢 One-to-Many (Place → Review)
    amenities = relationship("Amenity", secondary=place_amenity_association, back_populates="places")  # 🟢 Many-to-Many (Place ↔ Amenity)

    def __init__(self, title, description, price, latitude, longitude, owner_id):
        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner_id = owner_id

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

    def to_dict(self):
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

    def __repr__(self):
        return f"<Place {self.title} (Owner: {self.owner_id})>"

class Review(Base):
    """Review model for storing place reviews."""
    __tablename__ = 'reviews'

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    text = Column(String, nullable=False)
    rating = Column(Integer, nullable=False)
    place_id = Column(String(36), ForeignKey("places.id"), nullable=False)  # 🟢 One-to-Many (Place → Review)
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False)  # 🟢 One-to-Many (User → Review)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    place = relationship("Place", back_populates="reviews")  # 🟢 One-to-Many (Place → Review)
    user = relationship("User", back_populates="reviews")  # 🟢 One-to-Many (User → Review)

    def __init__(self, text, rating, place_id, user_id):
        self.text = text
        self.rating = rating
        self.place_id = place_id
        self.user_id = user_id

    @validates('rating')
    def validate_rating(self, key, rating):
        """Ensures the rating is between 1 and 5."""
        if rating < 1 or rating > 5:
            raise ValueError("Rating must be between 1 and 5.")
        return rating

    def to_dict(self):
        """Converts the review object to a dictionary."""
        return {
            "id": self.id,
            "text": self.text,
            "rating": self.rating,
            "place_id": self.place_id,
            "user_id": self.user_id,
            "created_at": self.created_at.isoformat(),
        }

    def __repr__(self):
        return f"<Review {self.text[:30]} (Rating: {self.rating})>"

class Amenity(Base):
    """Amenity model for storing place amenities."""
    __tablename__ = 'amenities'

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(50), nullable=False)

    # Many-to-Many (Place ↔ Amenity)
    places = relationship("Place", secondary=place_amenity_association, back_populates="amenities")

    def __init__(self, name):
        self.name = name

    @validates('name')
    def validate_name(self, key, name):
        """Ensures the name is not empty."""
        if not name or len(name.strip()) == 0:
            raise ValueError("Amenity name cannot be empty.")
        return name

    def to_dict(self):
        """Converts the amenity object to a dictionary."""
        return {
            "id": self.id,
            "name": self.name,
        }

    def __repr__(self):
        return f"<Amenity {self.name}>"