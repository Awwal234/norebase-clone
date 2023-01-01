from flask import Flask
from flask_restx import Api
from models.user import db
from .auth.auth import auth_namespace
from flask_jwt_extended import JWTManager


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///norebase.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'jdhfbcndsjkqeliqewu8iq39599'
    db.init_app(app)
    with app.app_context():
        db.create_all()
    api = Api(app)
    jwt = JWTManager(app)
    api.add_namespace(auth_namespace, path='/auth')

    return app
