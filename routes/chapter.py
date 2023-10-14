from controllers.auth.decorators import admin_required
from . import blueprint
from controllers import chapterController
from flask_jwt_extended import jwt_required,get_jwt,current_user
from flask import request


@blueprint.route('/chapter',methods=["GET"])
@blueprint.route('/chapter/<int:id>',methods=["GET"])
def getChapter(id=None):
    if id == None:
        return chapterController.getAll()
    return chapterController.get(id)
@blueprint.route('/chapter',methods=["POST"])
@blueprint.route('/chapter/<int:id>',methods=["DELETE","PUT"])
@admin_required()
def chapter(id=None):
    method = request.method

    if method == "POST":
        return chapterController.create()
    if method == "PUT":
        return chapterController.update(id)
    if method == "DELETE":
        return chapterController.softDelete(id)
