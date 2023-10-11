from . import blueprint
from controllers import categoryController
from flask_jwt_extended import jwt_required,get_jwt,current_user
from flask import request

@blueprint.route('/category',methods=['GET','POST'])
@blueprint.route('/category/<int:id>',methods=['GET','DELETE','PUT'])
def category(id=None):
    method=request.method
    if method=='GET':
        if id==None:
            return categoryController.getAll()
        else:
            return categoryController.get(id)
    if method == 'DELETE':
        #sementara jangan digunakan
        # return categoryController.delete(id)
        return 'temporarily cannot be used',404
    if method =='POST':
        return categoryController.create()
    if method == 'PUT':
        return categoryController.update(id)

