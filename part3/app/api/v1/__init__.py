from flask import Blueprint
from flask_restx import Api
from app.api.v1.users import api as users_namespace
from app.api.v1.amenities import api as amenities_namespace
from app.api.v1.places import api as places_namespace
from app.api.v1.auth import api as auth_namespace  # make sure this line is correct

blueprint = Blueprint('api_v1', __name__, url_prefix='/api/v1')

api = Api(
    blueprint,
    title='HBnB API',
    version='1.0',
    description='HBnB Application API'
)

api.add_namespace(users_namespace, path='/users')
api.add_namespace(amenities_namespace, path='/amenities')
api.add_namespace(places_namespace, path='/places')
api.add_namespace(auth_namespace, path='/auth')