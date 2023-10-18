import os
from controllers.auth.decorators import member_required
from . import blueprint
from controllers import enrollmentDetailController
from flask_jwt_extended import jwt_required,get_jwt,current_user
from flask import request, send_from_directory


@blueprint.route('/img/<path:filename>') 
def send_file(filename): 
    return send_from_directory(directory='public/uploaded_img/',path=filename)
