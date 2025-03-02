from flask import Blueprint
from flask_restx import Api

# Import the amenities namespace
from .amenities import api as amenities_namespace

# Create a Blueprint for the API
blueprint = Blueprint('api', __name__, url_prefix='/api')

# Initialize the API with documentation details
api = Api(
    blueprint,
    title='My API',
    version='1.0',
    description='API for managing amenities and other resources'
)

# Register the Amenities namespace
api.add_namespace(amenities_namespace, path='/amenities')

# Function to create the Flask app and register the blueprint
def create_app():
    from flask import Flask
    app = Flask(__name__)
    
    # Register the API blueprint
    app.register_blueprint(blueprint)

    return app