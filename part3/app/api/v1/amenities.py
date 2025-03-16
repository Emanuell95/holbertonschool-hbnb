from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt
from app.services import facade

api = Namespace('amenities', description='Amenity operations')

# Define the amenity model for input validation and documentation
amenity_model = api.model('Amenity', {
    'name': fields.String(required=True, description='Name of the amenity')
})

def admin_required():
    """Ensure the user is an admin"""
    claims = get_jwt()  # Get JWT claims
    if not claims.get("is_admin", False):
        return {"message": "Admin access required."}, 403

@api.route('/')
class AmenityList(Resource):
    @jwt_required()  # 🔒 Require authentication
    @api.expect(amenity_model)
    @api.response(201, 'Amenity successfully created')
    @api.response(400, 'Invalid input data')
    @api.response(403, 'Admin access required')
    def post(self):
        """Admin: Register a new amenity"""
        # 🔒 Ensure only admins can create amenities
        admin_check = admin_required()
        if admin_check:
            return admin_check  # Returns {"message": "Admin access required."}, 403

        data = api.payload

        # ✅ Create amenity
        new_amenity = facade.create_amenity(data)

        if not new_amenity:
            return {"message": "Invalid input data"}, 400

        return {"message": "Amenity successfully created", "amenity": new_amenity}, 201

    @api.response(200, 'List of amenities retrieved successfully')
    def get(self):
        """Retrieve a list of all amenities (Publicly accessible)"""
        amenities = facade.get_all_amenities()
        return amenities, 200

@api.route('/<amenity_id>')
class AmenityResource(Resource):
    @api.response(200, 'Amenity details retrieved successfully')
    @api.response(404, 'Amenity not found')
    def get(self, amenity_id):
        """Get amenity details by ID (Publicly accessible)"""
        amenity = facade.get_amenity_by_id(amenity_id)
        if not amenity:
            return {"message": "Amenity not found"}, 404
        return amenity, 200

    @jwt_required()  # 🔒 Require authentication
    @api.expect(amenity_model)
    @api.response(200, 'Amenity updated successfully')
    @api.response(404, 'Amenity not found')
    @api.response(400, 'Invalid input data')
    @api.response(403, 'Admin access required')
    def put(self, amenity_id):
        """Admin: Update an amenity's information"""
        # 🔒 Ensure only admins can update amenities
        admin_check = admin_required()
        if admin_check:
            return admin_check  # Returns {"message": "Admin access required."}, 403

        data = api.payload

        # 🔎 Check if the amenity exists
        existing_amenity = facade.get_amenity_by_id(amenity_id)
        if not existing_amenity:
            return {"message": "Amenity not found"}, 404

        # ✅ Update amenity
        updated_amenity = facade.update_amenity(amenity_id, data)

        if not updated_amenity:
            return {"message": "Invalid input data"}, 400

        return {"message": "Amenity updated successfully", "amenity": updated_amenity}, 200