from functools import wraps
from flask import jsonify, request
from flask_jwt_extended import create_access_token,create_refresh_token, get_jwt_identity,get_jwt, verify_jwt_in_request
from models import User,TokenBlocklist

def register():
    data=request.get_json()
    user=User.get_user_by_email(email=data.get('email'))
    if user is not None:
        return {'error':'email already used'},400
    user=User.get_user_by_username(username=data.get('username'))
    if user is not None:
        return {'error':'username already used'},400
    
    new_user=User(username=data.get('username'),
                  email=data.get('email'))
    new_user.set_password(data.get('password'))
    new_user.save()

    return new_user.as_dict(),201

def login():
    username = request.json.get("username",None)
    password = request.json.get("password", None)
    user=User.get_user_by_username(username)
    if not user:
        return {"msg": "Username not registered"}, 401
    if user.check_password(password) is False:
        return {"msg": "Wrong password"}, 401
    
    additional= {'role':user.role.role_name}

    access_token = create_access_token(identity=username,
                                       additional_claims=additional
                                       )
    refresh_token =create_refresh_token(identity=username,
                                        additional_claims=additional)
    # return jsonify(access_token=access_token)

    return {"msg":"Logged In",
            "tokens":{
                "access":access_token,
                "refresh":refresh_token
            }}


def refresh():
    identity= get_jwt_identity()
    j=get_jwt()
    new_access_token= create_access_token(identity=identity,additional_claims={'role':j.get('role')})
    return {"access_token":new_access_token},200


def logout():
    jwt=get_jwt()
    jti=jwt['jti']
    token_type=jwt['type']
    block= TokenBlocklist(jti=jti)
    block.save()
    return {'msg':f'{token_type} token revoked successfully'},200