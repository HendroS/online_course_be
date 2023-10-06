from . import blueprint
from controllers import authController
from flask_jwt_extended import jwt_required,get_jwt,get_jwt_identity,create_access_token
from models import TokenBlocklist

@blueprint.route('/register',methods=['POST'])
def register():
    result = authController.register()
    return result

@blueprint.route('/login',methods=['POST'])
def login():
    result = authController.login()
    return result

@blueprint.route('/refresh',methods=['GET'])
@jwt_required(refresh=True)
def refresh_access():
    identity= get_jwt_identity()
    new_access_token= create_access_token(identity=identity)
    return {"access_token":new_access_token},200

@blueprint.route('/logout')
@jwt_required(verify_type=False)
def logout():
    jwt=get_jwt()
    jti=jwt['jti']
    token_type=jwt['type']
    block= TokenBlocklist(jti=jti)
    block.save()
    return {'msg':f'{token_type} token revoked successfully'},200


@blueprint.route('/who',methods=['GET'])
@jwt_required()
def who():
    result= get_jwt()
    
    return result
