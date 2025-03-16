from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services import facade

api = Namespace('reviews', description='Review operations')

# Define the review model
review_model = api.model('Review', {
    'text': fields.String(required=True, description='Text of the review'),
    'rating': fields.Integer(required=True, description='Rating of the place (1-5)'),
    'place_id': fields.String(required=True, description='ID of the place')
})

@api.route('/')
class ReviewList(Resource):
    @jwt_required()  # 🔒 Require authentication
    @api.expect(review_model)
    @api.response(201, 'Review successfully created')
    @api.response(400, 'You cannot review your own place or already reviewed')
    def post(self):
        """Register a new review"""
        user_id = get_jwt_identity()  # ✅ Get the authenticated user ID
        data = api.payload
        place_id = data.get('place_id')

        # 🔎 Fetch the place to check ownership
        place = facade.get_place_by_id(place_id)
        if not place:
            return {"message": "Place not found"}, 404

        # ❌ Ensure the user is NOT reviewing their own place
        if place["owner_id"] == user_id:
            return {"message": "You cannot review your own place."}, 400

        # 🔎 Check if the user already reviewed this place
        existing_review = facade.get_review_by_user_and_place(user_id, place_id)
        if existing_review:
            return {"message": "You have already reviewed this place."}, 400

        # ✅ Proceed to create the review
        data['user_id'] = user_id  # Ensure the user ID is set correctly
        new_review = facade.create_review(data)

        if not new_review:
            return {"message": "Invalid input data"}, 400

        return {"message": "Review successfully created", "review": new_review}, 201

@api.route('/<review_id>')
class ReviewResource(Resource):
    @jwt_required()  # 🔒 Require authentication
    @api.expect(review_model)
    @api.response(200, 'Review updated successfully')
    @api.response(403, 'Unauthorized action')
    @api.response(404, 'Review not found')
    def put(self, review_id):
        """Update a review (Only the creator can modify it)"""
        user_id = get_jwt_identity()  # ✅ Get authenticated user ID

        # 🔎 Fetch the review to check ownership
        review = facade.get_review_by_id(review_id)
        if not review:
            return {"message": "Review not found"}, 404

        # ❌ Ensure the user owns this review
        if review["user_id"] != user_id:
            return {"message": "Unauthorized action."}, 403

        # ✅ Proceed to update the review
        data = api.payload
        updated_review = facade.update_review(review_id, data)

        if not updated_review:
            return {"message": "Invalid input data"}, 400

        return {"message": "Review updated successfully", "review": updated_review}, 200

    @jwt_required()  # 🔒 Require authentication
    @api.response(200, 'Review deleted successfully')
    @api.response(403, 'Unauthorized action')
    @api.response(404, 'Review not found')
    def delete(self, review_id):
        """Delete a review (Only the creator can delete it)"""
        user_id = get_jwt_identity()  # ✅ Get authenticated user ID

        # 🔎 Fetch the review to check ownership
        review = facade.get_review_by_id(review_id)
        if not review:
            return {"message": "Review not found"}, 404

        # ❌ Ensure the user owns this review
        if review["user_id"] != user_id:
            return {"message": "Unauthorized action."}, 403

        # ✅ Proceed to delete the review
        facade.delete_review(review_id)
        return {"message": "Review deleted successfully"}, 200