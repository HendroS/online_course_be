from controllers.auth.decorators import member_required
from . import blueprint
from controllers import enrollmentController
from flask_jwt_extended import jwt_required,get_jwt,current_user
from flask import request


@blueprint.route('/enrollment',methods=['GET',"POST"])
@blueprint.route('/enrollment/<uuid:id>',methods=["DELETE","PUT"])
@member_required()
def enrollment(id=None):
    method = request.method
    if method == "GET":
        enrolls= enrollmentController.getAll()
        return enrolls
    if method == "POST":
        enroll = enrollmentController.create()
        return enroll
    if method == "DELETE":
        enroll = enrollmentController.delete(id)
        return enroll
    if method =="PUT":
        enroll = enrollmentController.update(id)
        return enroll
    
