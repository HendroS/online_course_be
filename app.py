import os
from flask import Flask
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy

from routes import blueprint
# from controller import db

load_dotenv()

db = SQLAlchemy()
# configure the SQLite database, relative to the app instance folder

# initialize the app with the extension
def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv('DB_URI_ONLINECOURSE')
    db.init_app(app)

    # with app.app_context():
    #     print('coba aja test')

    app.register_blueprint(blueprint)



    return app