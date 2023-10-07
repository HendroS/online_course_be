import os
from flask import Flask
from dotenv import load_dotenv

from routes import blueprint
from models import User,TokenBlocklist
from extensions import db,jwt

load_dotenv()


# initialize the app with the extension
def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv('FLASK_DB_URI_ONLINECOURSE')
    app.config["JWT_SECRET_KEY"] = os.getenv('FLASK_JWT_SECRET_KEY')
    app.config["JWT_ALGORITHM"] = os.getenv('FLASK_JWT_ALGHORITHM')
    db.init_app(app)
    jwt.init_app(app)

    with app.app_context():
        print('create db')
        db.create_all()

    app.register_blueprint(blueprint)


    @jwt.user_lookup_loader
    def user_look_up(__jwt_headers,jwt_data):
        identity=jwt_data['sub']
        return User.get_user_by_username(identity)

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header,jwt_data):
        return {"msg":"Token has Expired","error":"token_expired"}
    
    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return {"msg":"Signature verification failed","error":"invalid_token"}
    
    @jwt.unauthorized_loader
    def unauthorized_callback(error):
        return {"msg":"Request doesnt contain a valid token","error":"authorization_header"}

    @jwt.token_in_blocklist_loader
    def token_blocklist_callback(jwt_header,jwt_data):
        jti=jwt_data['jti']
        token= TokenBlocklist.get_by_jti(jti)
        return token is not None




    return app