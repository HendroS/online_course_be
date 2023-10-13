from . import blueprint
from controllers import enrollmentDetailController
from flask_jwt_extended import jwt_required,get_jwt,current_user
from flask import request


@blueprint.route('/enrollmentchapter',methods=['GET','POST'])
@blueprint.route('/enrollmentchapter/<int:enrollment_id>',methods=['GET','PUT'])
def detail(enrollment_id=None):
    method = request.method
    if method == 'GET':
        if enrollment_id == None:
            return enrollmentDetailController.getAll()
        return enrollmentDetailController.get(enrollment_id)
    
    if method == 'POST':
        return enrollmentDetailController.create()
    
    if method == 'PUT':
        return enrollmentDetailController.complete(enrollment_id)