from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_uuid import FlaskUUID
db = SQLAlchemy()
jwt=JWTManager()
flask_uuid= FlaskUUID()