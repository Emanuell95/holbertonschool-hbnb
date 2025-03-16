from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.services import facade
from app.utils.security import hash_password

api = Namespace('users', description='User operations')

# Define the user model for input validation and documentation
user_model = api.model('User', {
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user'),
    'password': fields.String(required=True, description='Password of the user'),
    'is_admin': fields.Boolean(description="Admin privileges (True/False)")
})

update_user_model = api.model('UpdateUser', {
    'first_name': fields.String(description='First name of the user'),
    'last_name': fields.String(description='Last name of the user'),
    'email': fields.String(description='New email of the user (Admins only)'),
    'password': fields.String(description='New password of the user (Admins only)')
})

def admin_required():
    """Ensure the user is an admin"""
    claims = get_jwt()  # Get JWT claims
    if not claims.get("is_admin", False):
        return {"message": "Admin access required."}, 403

@api.route('/')
class UserList(Resource):
    @jwt_required()  # 🔒 Require authentication
    @api.expect(user_model, validate=True)
    @api.response(201, 'User successfully created')
    @api.response(400, 'Email already registered')
    @api.response(403, 'Admin access required')
    def post(self):
        """Admin: Create a new user"""
        # 🔒 Ensure only admins can create users
        admin_check = admin_required()
        if admin_check:
            return admin_check  # Returns {"message": "Admin access required."}, 403

        user_data = api.payload

        # 🔎 Check if email is already registered
        existing_user = facade.get_user_by_email(user_data['email'])
        if existing_user:
            return {'error': 'Email already registered'}, 400

        # ✅ Hash password before storing
        user_data['password'] = hash_password(user_data['password'])

        # ✅ Create user
        new_user = facade.create_user(user_data)

        return {'id': new_user.id, 'message': 'User successfully created'}, 201

@api.route('/<string:user_id>')
@api.param('user_id', 'The User identifier')
class User(Resource):
    @api.response(200, 'Success')
    @api.response(404, 'User not found')
    def get(self, user_id):
        """Retrieve user details by ID (excluding password)"""
        user = facade.get_user_by_id(user_id)
        if not user:
            api.abort(404, 'User not found')

        return {
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email
        }, 200

    @jwt_required()  # 🔒 Require authentication
    @api.expect(update_user_model)
    @api.response(200, 'User updated successfully')
    @api.response(400, 'You cannot modify email or password.')
    @api.response(403, 'Unauthorized action')
    @api.response(404, 'User not found')
    def put(self, user_id):
        """Modify user information"""
        auth_user_id = get_jwt_identity()  # ✅ Get authenticated user ID
        claims = get_jwt()  # ✅ Get JWT claims

        # 🔎 Fetch the user to ensure they exist
        user = facade.get_user_by_id(user_id)
        if not user:
            return {"message": "User not found"}, 404

        update_data = api.payload

        # 🔒 Admins can modify any user (including email & password)
        if claims.get("is_admin", False):
            # 🔎 Check if email is already taken
            if "email" in update_data:
                existing_user = facade.get_user_by_email(update_data["email"])
                if existing_user and existing_user.id != user_id:
                    return {"message": "Email already registered."}, 400

            # ✅ Hash the new password if provided
            if "password" in update_data:
                update_data["password"] = hash_password(update_data["password"])

            updated_user = facade.update_user(user_id, update_data)
            return {"message": "User updated successfully", "user": updated_user}, 200

        # ❌ Regular users can only modify their own profile (excluding email/password)
        if user_id != auth_user_id:
            return {"message": "Unauthorized action."}, 403

        if "email" in update_data or "password" in update_data:
            return {"message": "You cannot modify email or password."}, 400

        updated_user = facade.update_user(user_id, update_data)
        return {"message": "User updated successfully", "user": updated_user}, 200