from . import blueprint
from controllers import instructorController
from flask_jwt_extended import jwt_required,get_jwt,current_user
from flask import request

@blueprint.route('/instructor',methods=['GET',"POST"])
@blueprint.route('/instructor/<int:id>',methods=["GET","DELETE","PUT"])
def instructor(id=None):
    method = request.method
    if method == "GET":
        if id == None:
            return instructorController.getAll()
        return instructorController.get(id)
        
    if method == "POST":
        return instructorController.create()
        
    if method == "DELETE":
        # return instructorController.delete(id)
        return instructorController.softDelete(id)
        
    if method =="PUT":
       
        return instructorController.update(id)
        
    
