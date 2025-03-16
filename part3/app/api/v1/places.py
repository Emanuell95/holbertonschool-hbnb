from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services import facade

api = Namespace('places', description='Place operations')

# Models
amenity_model = api.model('PlaceAmenity', {
    'id': fields.String(description='Amenity ID'),
    'name': fields.String(description='Name of the amenity')
})

user_model = api.model('PlaceUser', {
    'id': fields.String(description='User ID'),
    'first_name': fields.String(description='First name of the owner'),
    'last_name': fields.String(description='Last name of the owner'),
    'email': fields.String(description='Email of the owner')
})

review_model = api.model('PlaceReview', {
    'id': fields.String(description='Review ID'),
    'text': fields.String(description='Text of the review'),
    'rating': fields.Integer(description='Rating of the place (1-5)'),
    'user_id': fields.String(description='ID of the user')
})

place_model = api.model('Place', {
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude of the place'),
    'longitude': fields.Float(required=True, description='Longitude of the place'),
    'amenities': fields.List(fields.String, required=True, description="List of amenities ID's"),
    'owner': fields.Nested(user_model, description='Owner of the place'),
    'reviews': fields.List(fields.Nested(review_model), description='List of reviews')
})

@api.route('/')
class PlaceList(Resource):
    @jwt_required()  # 🔒 Requires authentication for creating a place
    @api.expect(place_model)
    @api.response(201, 'Place successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new place"""
        user_id = get_jwt_identity()  # Get the logged-in user ID

        data = api.payload  # Get request data
        data['owner_id'] = user_id  # Ensure the authenticated user is the owner

        # Call service layer to create the place
        new_place = facade.create_place(data)

        if not new_place:
            return {"message": "Invalid input data"}, 400

        return {"message": "Place successfully created", "place": new_place}, 201

    @api.response(200, 'List of places retrieved successfully')
    def get(self):
        """Retrieve a list of all places (Publicly accessible)"""
        places = facade.get_all_places()
        return places, 200


@api.route('/<place_id>')
class PlaceResource(Resource):
    @api.response(200, 'Place details retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Retrieve detailed information about a specific place (Publicly accessible)"""
        place = facade.get_place_by_id(place_id)
        if not place:
            return {"message": "Place not found"}, 404
        return place, 200

    @jwt_required()  # 🔒 Requires authentication for updating a place
    @api.expect(place_model)
    @api.response(200, 'Place updated successfully')
    @api.response(404, 'Place not found')
    @api.response(403, 'Unauthorized to modify this place')
    @api.response(400, 'Invalid input data')
    def put(self, place_id):
        """Update a place's information (Only the owner can update)"""
        user_id = get_jwt_identity()  # Get the authenticated user ID

        # Fetch the place to check ownership
        place = facade.get_place_by_id(place_id)
        if not place:
            return {"message": "Place not found"}, 404

        # Ensure the authenticated user is the owner
        if place["owner_id"] != user_id:
            return {"message": "You are not authorized to modify this place"}, 403

        # Get updated data from request payload
        data = api.payload
        updated_place = facade.update_place(place_id, data)

        if not updated_place:
            return {"message": "Invalid input data"}, 400

        return {"message": "Place updated successfully", "place": updated_place}, 200