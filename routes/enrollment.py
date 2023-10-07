from . import blueprint
from controllers import enrollmentController
from flask_jwt_extended import jwt_required,get_jwt,current_user
from flask import request


@blueprint.route('/enrollment',methods=['GET',"POST"])
@blueprint.route('/enrollment/<int:course_id>',methods=["DELETE","PUT"])
def enrollment(course_id=None):
    method = request.method
    if method == "GET":
        enrolls= enrollmentController.getAll()
        return enrolls
    if method == "POST":
        enroll = enrollmentController.create()
        return enroll
    if method == "DELETE":
        enroll = enrollmentController.delete(course_id=course_id)
        return enroll
    if method =="PUT":
        print(course_id)
        enroll = enrollmentController.update(course_id=course_id)
        return enroll
    
