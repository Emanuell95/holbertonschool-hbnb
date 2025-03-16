from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, validates

Base = declarative_base()

# Many-to-Many Association Table (Place ↔ Amenity)
place_amenity_association = Table(
    "place_amenity",
    Base.metadata,
    Column("place_id", Integer, ForeignKey("places.id"), primary_key=True),
    Column("amenity_id", Integer, ForeignKey("amenities.id"), primary_key=True)
)

class Amenity(Base):
    """Amenity model for storing amenity details."""
    __tablename__ = 'amenities'

    id = Column(Integer, primary_key=True, autoincrement=True)  #Integer Auto-Increment
    name = Column(String(50), nullable=False, unique=True)  #Ensures names are unique
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    #Many-to-Many (Place ↔ Amenity)
    places = relationship("Place", secondary=place_amenity_association, back_populates="amenities")

    def __init__(self, name):
        self.name = name  # Assign name directly, validation will be handled

    @validates("name")
    def validate_name(self, key, value):
        """Ensure the name is between 1 and 50 characters and not empty."""
        if not value or len(value.strip()) == 0:
            raise ValueError("Amenity name cannot be empty.")
        if len(value) > 50:
            raise ValueError("Amenity name must be between 1 and 50 characters.")
        return value

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