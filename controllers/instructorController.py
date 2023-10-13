from flask import abort, request
from models import Instructor
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
    data=request.get_json()

    instructor=Instructor(instructor_name=data.get('instructor_name'),
                          description=data.get('description'),
                          image=data.get('image')
                          )
    instructor.save()
    return instructor.as_dict(),201
def update(id):
    data=request.get_json()
    instructor= Instructor.query.filter_by(instructor_id=id).first_or_404()

    instructor.instructor_name=data.get('instructor_name')
    instructor.description=data.get('description')
    instructor.image=data.get('image')    
    instructor.save()
    return instructor.as_dict()

def softDelete(id):
    instructor= Instructor.query.filter_by(instructor_id=id).first_or_404()
    instructor.is_active= False
    instructor.save()
    return {'msg':'soft delete success'}