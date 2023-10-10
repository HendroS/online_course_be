from . import blueprint
from controllers import courseController, enrollmentController
from flask_jwt_extended import jwt_required,get_jwt,current_user
from flask import request


@blueprint.route('/course',methods=['GET','POST'])
@blueprint.route('/course/<int:id>',methods=['GET','PUT'])
@jwt_required()
def course(id=None):
    method = request.method
    if method == "GET":
        if id == None:
            return courseController.get_all()
        return courseController.get(id)
    if method == "POST":
        return courseController.create()
    if method == "PUT":
        return courseController.update(id)

@blueprint.route('/course_active/<int:id>',methods=['PUT'])
def switch_active(id):
    return courseController.switch_active(id)

@blueprint.route('/course/top',methods=["GET"])
def top_enrollment():
    enrolls = courseController.getTopCourses()
    return enrolls
