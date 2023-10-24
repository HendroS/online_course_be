from controllers.auth.decorators import admin_required
from . import blueprint
from controllers import courseController
from flask_jwt_extended import jwt_required,get_jwt,current_user
from flask import request

@blueprint.route('/course',methods=['GET'])
@blueprint.route('/course/<uuid:id>',methods=['GET'])
def getCourse(id=None):
    if id == None:
        return courseController.get_all()
    return courseController.get(id)

@blueprint.route('/course',methods=['POST'])
@blueprint.route('/course/<uuid:id>',methods=['PUT'])
@admin_required()
def course(id=None):
    method = request.method
    if method == "POST":
        return courseController.create()
    if method == "PUT":
        return courseController.update(id)

@blueprint.route('/course_active/<uuid:id>',methods=['PUT'])
@admin_required()
def switch_active(id):
    return courseController.switch_active(id)

@blueprint.route('/course/top',methods=["GET"])
def top_enrollment():
    enrolls = courseController.getTopCourses()
    return enrolls

@blueprint.route('/course/advancesearch',methods=["GET"])
def advanceSearchCourse():
    courses=courseController.advanceSearch()
    return courses


@blueprint.route('/course/search',methods=["GET"])
def searchCourse():
    courses=courseController.search()
    return courses
