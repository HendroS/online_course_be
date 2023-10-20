import os
from uuid import uuid4
from flask import abort, request
from models import Instructor
from werkzeug.utils import secure_filename
# from flask_jwt_extended import current_user
# from helpers.utils import checkField

def getAll():
    instructors=Instructor.get_all()
    return {"instructors":[instructor.as_dict() for instructor in instructors]}

def get(id:int):
    instructor= Instructor.query.filter_by(instructor_id=id).first_or_404()
    return instructor.as_dict()

def delete(id:int):
    instructor= Instructor.query.filter_by(instructor_id=id).first_or_404()
    instructor.delete()
    return {'msg':'delete success'}

def create():
    # data=request.get_json()
    data= request.form
    instructor_name = data.get('instructor_name')
    description = data.get('description')
    image = request.files.get('image')

    if instructor_name == None:
        return {'msg':'instructor_name required'},400
    
    instructor=Instructor(instructor_name=instructor_name)

    if description != None:
        instructor.description=description
    
    if image != None:
        filename= secure_filename(f"{uuid4().hex}.{image.filename.split('.')[-1]}")
        path= os.path.join('public/uploaded_img/instructor',filename)
        image.save(path)
        instructor.image=filename


    instructor.save()
    return instructor.as_dict(),201
def update(id):
    # data=request.get_json()
    data= request.form
    instructor_name = data.get('instructor_name')
    description = data.get('description')
    image = request.files.get('image')

    instructor= Instructor.query.filter_by(instructor_id=id).first_or_404()
    if instructor_name != None:
        instructor.instructor_name=instructor_name

    if description != None:
        instructor.description=description

    if image != None:
        filename= secure_filename(f"{uuid4().hex}.{image.filename.split('.')[-1]}")
        path= os.path.join('public/uploaded_img/instructor',filename)
        image.save(path)
        old_image= instructor.image

        if old_image != None:
            old_path= os.path.join('public/uploaded_img/instructor',old_image)
            os.unlink(old_path)

        instructor.image=filename   

    instructor.save()
    return instructor.as_dict()

def softDelete(id):
    instructor= Instructor.query.filter_by(instructor_id=id).first_or_404()
    instructor.is_active= False
    instructor.save()
    return {'msg':'soft delete success'}