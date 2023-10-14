from flask import abort, request
from models import User,Role
from flask_jwt_extended import current_user

def getAll():
    users= User.query.all()
    return [{'username':user.username,
             'enrolls': [{'course':e.course.course_name,
                          'status':'completed' if e.is_completed is True else 'uncompleted'
                          } for e in user.enrolls]
             } for user in users],200
def get(id):
    result = User.get_user_by_id(id)
   
    user =result.as_dict()
    # user['enrolls']=[e.enrolls.]
    user['enrolls']=[{'course':e.course.course_name,
                      'status':'completed' if e.is_completed == True else 'uncompleted'} for e in result.enrolls]
    user.pop('password')
    return user

def update(id):
    if current_user.user_id != id:
        return {'msg':'Cant update other account'},403
    data=request.get_json()
    email = data.get("email",None)
    username = data.get("username",None)
    password = data.get("password", None)
    role_id= data.get("role_id", None)
    # columns=[email,username,password,role_id]
    user=User.get_user_by_id(id)
    if user is None:
        abort(404)

    
    if email != None and user.email.lower() != email.lower():
        user_mail= User.get_user_by_email(email.lower())
        if user_mail != None:
            return {'msg':'email already used'},400
        user.email = str(email).lower()
    
    if username != None and user.username != username:
        user_username = User.get_user_by_username(username)
        if user_username != None:
            return {'msg':'username already used'},400
    if password != None:
        user.password = password

    if role_id != None:
        if current_user.role.role_name != 'admin':
            return {'msg':'only admin allowed to change role'},400
        if not isinstance(role_id,int):
            return {'msg':'invalid role_id'},400
        role= Role.get_by_id(role_id)
        if role == None:
            return {'msg':"role_id not valid"},400
        user.role_id = role_id
    
    user.save()

    return user.as_dict()


def getTopUserEnroll():
    users= User.get_top_enrolled()
    return {'users':[dict(user) for user in users]}