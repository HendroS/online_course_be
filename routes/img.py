import os
from controllers.auth.decorators import member_required
from . import blueprint
from controllers import enrollmentDetailController
from flask_jwt_extended import jwt_required,get_jwt,current_user
from flask import request, send_from_directory


@blueprint.route('/img/category/<path:filename>') 
def send_category_pict(filename): 
    return send_from_directory(directory='public/uploaded_img/category',path=filename)

@blueprint.route('/img/profile/<path:filename>')
def send_profile_pict(filename):
    return send_from_directory(directory='public/uploaded_img/profile',path=filename)

@blueprint.route('/img/chapter/<path:filename>')
def send_chapter_image(filename):
    return send_from_directory(directory='public/uploaded_img/chapter',path=filename)