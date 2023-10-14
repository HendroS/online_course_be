from controllers.auth.decorators import admin_required
from . import blueprint
from controllers import instructorController
from flask_jwt_extended import jwt_required,get_jwt,current_user
from flask import request


@blueprint.route('/instructor',methods=["GET"])
@blueprint.route('/instructor/<int:id>',methods=["GET"])
def getInstructor(id=None):
    if id == None:
        return instructorController.getAll()
    return instructorController.get(id)

@blueprint.route('/instructor',methods=["POST"])
@blueprint.route('/instructor/<int:id>',methods=["DELETE","PUT"])
@admin_required()
def instructor(id=None):
    method = request.method

    if method == "POST":
        return instructorController.create()
        
    if method == "DELETE":
        # return instructorController.delete(id)
        return instructorController.softDelete(id)
        
    if method =="PUT":
       
        return instructorController.update(id)
        
    
