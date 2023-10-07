from . import blueprint
from controllers import userController
from flask_jwt_extended import jwt_required,get_jwt,current_user
from flask import request


@blueprint.route('/user',methods=['GET'])
@blueprint.route('/user/<int:id>',methods=['GET','PUT'])
@jwt_required()
def user(id=None):
    method= request.method
    if method=='GET':
        if id is None:
        # claims= get_jwt()
        # print(current_user)
        # if claims.get('role') is not 'admin':
        #     return 'you are not authorized',401
            result = userController.getAll()
        else:
            result = userController.get(id)
        return result
    if method=='PUT':
        result = userController.update(id)
        return result