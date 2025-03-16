from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity
from app.persistence.repository import SQLAlchemyRepository  
from app.utils.security import hash_password
from app.persistence import UserRepository 

class HBnBFacade:
    def __init__(self):
        """Initialize repositories for each entity"""
        self.user_repo = UserRepository()  
        self.place_repo = SQLAlchemyRepository(Place)
        self.review_repo = SQLAlchemyRepository(Review)
        self.amenity_repo = SQLAlchemyRepository(Amenity)

    
    def create_user(self, user_data):
        """Create a new user, hash password, and store in the database"""
        if self.user_repo.is_email_registered(user_data["email"]):
            return {"error": "Email already registered"}, 400  
        
        user = User(**user_data)
        user.password = hash_password(user_data['password'])  
        return self.user_repo.add(user)

    def get_user_by_id(self, user_id):
        """Retrieve user by ID"""
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        """Retrieve user by email"""
        return self.user_repo.get_user_by_email(email)

    def update_user(self, user_id, user_data):
        """Update user details (excluding password & email for non-admins)"""
        return self.user_repo.update(user_id, user_data)

    def delete_user(self, user_id):
        """Delete a user"""
        return self.user_repo.delete(user_id)

    
    def create_place(self, place_data):
        """Create a new place"""
        place = Place(**place_data)
        return self.place_repo.add(place)

    def get_place_by_id(self, place_id):
        """Retrieve place details by ID"""
        return self.place_repo.get(place_id)

    def update_place(self, place_id, place_data):
        """Update place details"""
        return self.place_repo.update(place_id, place_data)

    def delete_place(self, place_id):
        """Delete a place"""
        return self.place_repo.delete(place_id)

    
    def create_review(self, review_data):
        """Create a new review"""
        review = Review(**review_data)
        return self.review_repo.add(review)

    def get_review_by_id(self, review_id):
        """Retrieve a review by ID"""
        return self.review_repo.get(review_id)

    def update_review(self, review_id, review_data):
        """Update a review"""
        return self.review_repo.update(review_id, review_data)

    def delete_review(self, review_id):
        """Delete a review"""
        return self.review_repo.delete(review_id)

    
    def create_amenity(self, amenity_data):
        """Create a new amenity"""
        amenity = Amenity(**amenity_data)
        return self.amenity_repo.add(amenity)

    def get_amenity_by_id(self, amenity_id):
        """Retrieve an amenity by ID"""
        return self.amenity_repo.get(amenity_id)

    def update_amenity(self, amenity_id, amenity_data):
        """Update an amenity"""
        return self.amenity_repo.update(amenity_id, amenity_data)

    def delete_amenity(self, amenity_id):
        """Delete an amenity"""
        return self.amenity_repo.delete(amenity_id)