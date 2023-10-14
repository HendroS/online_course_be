from controllers.auth.decorators import admin_required
from . import blueprint
from controllers import userController
from flask_jwt_extended import jwt_required,get_jwt,current_user
from flask import request


@blueprint.route('/user',methods=['GET'])
@admin_required()
def allUser():
    return userController.getAll()

@blueprint.route('/user/<int:id>',methods=['GET','PUT'])
@jwt_required()
def user(id):
    method= request.method
    if method=='GET':
        return userController.get(id)
    
    if method=='PUT':
        return userController.update(id)
    
@blueprint.route('/user/top',methods=['GET'])
@admin_required()
def getTopUserEnroll():
    return userController.getTopUserEnroll()
    
