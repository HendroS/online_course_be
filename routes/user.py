from . import blueprint
from controllers import userController
from flask_jwt_extended import jwt_required,get_jwt,current_user


@blueprint.route('/user',methods=['GET'])
@jwt_required()
def user():
    claims= get_jwt()
    # print(current_user)
    # if claims.get('role') is not 'admin':
    #     return 'you are not authorized',401
    result = userController.getAll()
    return result