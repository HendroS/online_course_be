from flask import Blueprint

blueprint = Blueprint('my_blueprint', __name__)

from . import auth,user,course,enrollment,category,chapter,instructor,enrollmentDetail