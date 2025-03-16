from app.models.user import User
from app.persistence.repository import SQLAlchemyRepository
from app import db

class UserRepository(SQLAlchemyRepository):
    def __init__(self):
        """Initialize the UserRepository with the User model"""
        super().__init__(User)

    def get_user_by_email(self, email):
        """Find a user by email"""
        return self.model.query.filter_by(email=email).first()

    def is_email_registered(self, email):
        """Check if an email is already registered (returns True/False)"""
        return self.model.query.filter_by(email=email).first() is not None