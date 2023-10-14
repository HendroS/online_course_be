from . import blueprint
from controllers import categoryController
from flask_jwt_extended import jwt_required,get_jwt,current_user
from flask import request
from controllers.auth.decorators import admin_required

@blueprint.route('/category',methods=['GET'])
@blueprint.route('/category/<int:id>',methods=['GET'])
def getCategory(id=None):
    if id==None:
        return categoryController.getAll()
    else:
        return categoryController.get(id)

@blueprint.route('/category',methods=['POST'])
@blueprint.route('/category/<int:id>',methods=['DELETE','PUT'])
@admin_required()
def category(id=None):
    method=request.method
    if method == 'DELETE':
        #sementara jangan digunakan
        # return categoryController.delete(id)
        return 'temporarily cannot be used',404
    if method =='POST':
        return categoryController.create()
    if method == 'PUT':
        return categoryController.update(id)

