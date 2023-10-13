from . import blueprint
from controllers import chapterController
from flask_jwt_extended import jwt_required,get_jwt,current_user
from flask import request

@blueprint.route('/chapter',methods=["GET","POST"])
@blueprint.route('/chapter/<int:id>',methods=["GET","DELETE","PUT"])
def chapter(id=None):
    method = request.method
    if method == "GET":
        if id == None:
            return chapterController.getAll()
        return chapterController.get(id)
    if method == "POST":
        return chapterController.create()
    if method == "PUT":
        return chapterController.update(id)
    if method == "DELETE":
        return chapterController.softDelete(id)
