from . import blueprint
from controllers import authController
from flask_jwt_extended import jwt_required,get_jwt,get_jwt_identity,create_access_token
from models import TokenBlocklist

@blueprint.route('/register',methods=['POST'])
def register():
    return authController.register()
   

@blueprint.route('/login',methods=['POST'])
def login():
    return authController.login()

@blueprint.route('/refresh',methods=['GET'])
@jwt_required(refresh=True)
def refresh_access():
    return authController.refresh()


@blueprint.route('/logout')
@jwt_required(verify_type=False)
def logout():
    return authController.logout()


@blueprint.route('/who',methods=['GET'])
@jwt_required()
def who():
    return get_jwt()

