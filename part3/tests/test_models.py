import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from ..app.models.base_model import Base
from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

# Ensure the app module is recognized
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

# Use an in-memory SQLite database for testing
TEST_DATABASE_URI = "sqlite:///:memory:"

def setup_test_session():
    """Setup a new test database session."""
    engine = create_engine(TEST_DATABASE_URI)
    Base.metadata.create_all(engine)
    TestingSessionLocal = sessionmaker(bind=engine)
    return TestingSessionLocal()

@pytest.fixture(scope="function")
def test_session():
    session = setup_test_session()
    yield session
    session.close()

# Test User Model
def test_user_creation(test_session):
    user = User(first_name="John", last_name="Doe", email="john.doe@example.com")
    test_session.add(user)
    test_session.commit()
    retrieved_user = test_session.query(User).filter_by(email="john.doe@example.com").first()
    assert retrieved_user is not None
    assert retrieved_user.first_name == "John"
    assert retrieved_user.last_name == "Doe"
    assert retrieved_user.email == "john.doe@example.com"
    assert retrieved_user.is_admin is False

# Test Place Model
def test_place_creation(test_session):
    owner = User(first_name="Alice", last_name="Smith", email="alice@example.com")
    test_session.add(owner)
    test_session.commit()
    place = Place(title="Cozy Apartment", description="Nice place", price=100.0, latitude=37.7749, longitude=-122.4194, owner=owner)
    test_session.add(place)
    test_session.commit()
    retrieved_place = test_session.query(Place).filter_by(title="Cozy Apartment").first()
    assert retrieved_place is not None
    assert retrieved_place.owner.email == "alice@example.com"

# Test Review Model
def test_review_creation(test_session):
    user = User(first_name="Charlie", last_name="Brown", email="charlie@example.com")
    test_session.add(user)
    test_session.commit()
    place = Place(title="Beach House", description="Ocean view", price=200.0, latitude=34.0522, longitude=-118.2437, owner=user)
    test_session.add(place)
    test_session.commit()
    review = Review(text="Amazing experience!", rating=5, place=place, user=user)
    test_session.add(review)
    test_session.commit()
    retrieved_review = test_session.query(Review).filter_by(text="Amazing experience!").first()
    assert retrieved_review is not None
    assert retrieved_review.rating == 5
    assert retrieved_review.place.title == "Beach House"

# Test Amenity Model
def test_amenity_creation(test_session):
    amenity = Amenity(name="Wi-Fi")
    test_session.add(amenity)
    test_session.commit()
    retrieved_amenity = test_session.query(Amenity).filter_by(name="Wi-Fi").first()
    assert retrieved_amenity is not None
    assert retrieved_amenity.name == "Wi-Fi"

# Test Place and Amenity Relationship
def test_add_amenity_to_place(test_session):
    user = User(first_name="Diana", last_name="Prince", email="diana@example.com")
    test_session.add(user)
    test_session.commit()
    place = Place(title="Luxury Villa", description="Beautiful property", price=500.0, latitude=35.6895, longitude=139.6917, owner=user)
    test_session.add(place)
    test_session.commit()
    wifi = Amenity(name="Wi-Fi")
    pool = Amenity(name="Swimming Pool")
    place.amenities.append(wifi)
    place.amenities.append(pool)
    test_session.commit()
    retrieved_place = test_session.query(Place).filter_by(title="Luxury Villa").first()
    assert retrieved_place is not None
    assert len(retrieved_place.amenities) == 2
