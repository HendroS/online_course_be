import os
from uuid import uuid4
from flask import abort, request
from models import User,Role
from flask_jwt_extended import current_user
from werkzeug.utils import secure_filename
from helpers.utils import checkValidUUID

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
    # data=request.get_json()
    data=request.form
    email = data.get("email",None)
    username = data.get("username",None)
    password = data.get("password", None)
    role_id= data.get("role_id", None)
    image=request.files.get('image')


    user=User.get_user_by_id(id)
    if user is None:
        abort(404)

    
    if email != None and user.email.lower() != email.lower():
        user_mail= User.get_user_by_email(email.lower())
        if user_mail != None:
            return {'msg':'email already used'},400
        user.email = str(email).lower()
    # print(username)
    if username != None and user.username != username.strip():
        user_username = User.get_user_by_username(username)
        if user_username != None:
            return {'msg':'username already used'},400
        user.username = username.strip()
        
    if password != None:
        user.set_password(password)

    if role_id != None:
        if current_user.role.role_name != 'admin':
            return {'msg':'only admin allowed to change role'},400
        
        if not checkValidUUID(role_id):
            return {'msg':'role_id not valid'},400

        role= Role.get_by_id(role_id)
        if role == None:
            return {'msg':"role_id not found"},400
        user.role_id = role_id

    if image != None:
        filename= secure_filename(f"{uuid4().hex}.{image.filename.split('.')[-1]}")
        path= os.path.join('public/uploaded_img/profile',filename)
        image.save(path)
        old_image= user.image

        user.image= filename
        if old_image != None:
            old_path = os.path.join('public/uploaded_img/profile',filename)
            os.unlink(old_path)
    
    user.save()

    return user.as_dict()


def getTopUserEnroll():
    users= User.get_top_enrolled()
    return {'users':[dict(user) for user in users]}