import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(__file__)))
from app import create_app
from app.api.v1 import api
from app.api.v1.places import api as places_ns
from flask import Flask
from flask_restx import Api
from flask_cors import CORS
from app.persistence.repository import db

# Importing API namespaces
from app.api.v1.places import api as places_ns
from app.api.v1.users import api as users_ns
from app.api.v1.amenities import api as amenities_ns

app = Flask(__name__)
CORS(app)

app = create_app()
with app.app_context():
    db.create_all()

api.add_namespace(places_ns, path='/api/v1/places')

api.add_namespace(places_ns, path='/api/v1/places')
api.add_namespace(users_ns, path='/api/v1/users')
api.add_namespace(amenities_ns, path='/api/v1/amenities')

if __name__ == '__main__':
    app.run(debug=True, port=5000)