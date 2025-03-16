from flask import Flask
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from app.persistence.repository import db
from app.api.v1 import api as api_v1
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

bcrypt = Bcrypt()
jwt = JWTManager()

def create_app(config_class="config.DevelopmentConfig"):
    app = Flask(__name__)
    
    # FIRST: Configure your app settings clearly and explicitly before init_db
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///yourdb.sqlite3'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = 'your_secret_key_here'

    # THEN initialize your extensions
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    # THEN register your API blueprint
    app.register_blueprint(api_v1.blueprint, url_prefix='/api/v1')

    return app