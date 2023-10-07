from flask import abort, request
from models import Course,Category
from flask_jwt_extended import current_user
from helpers.utils import checkField 


def get(id):
    course=Course.get_course_by_id(id)
    return course.as_dict(),200

def get_all():
    select= request.args.get('select','all')
    if select.lower() == 'inactive':  
        courses=Course.get_all_with_active_status(False)
    elif select.lower() == 'active':
        courses=Course.get_all_with_active_status(True)
    else :  
        courses=Course.get_all()
    return {'courses':[course.as_dict() for course in courses]},200

def create():
    data = request.get_json()
    required=['category_id','course_name']
    not_present= checkField(required,data)
    if len(not_present)>0:
        return {'msg':f'field {", ".join(not_present)} are required.'},400
    category=Category.get_category_by_id(data.get('category_id'))
    if category == None:
        return {'msg': f'category_id {data.get("category_id")} is not found in database'},400
    course = Course(category_id=data.get("category_id"),
                    course_name = data.get("course_name"))
    if data.get('description') != None:
        course.description = data.get('description')
    course.save()
    return course.as_dict(),201

def delete(id):
    course = Course.get_course_by_id(id)
    course.delete()
    return {'msg':'delete success'},200

def update(id):
    data = request.get_json()
    course =Course.get_course_by_id(id)

    if data.get('description') != None:
        course.description = data.get('description')
    
    if data.get('category_id') != None:
        category=Category.get_category_by_id(data.get('category_id'))
        if category == None:
            return {'msg': f'category_id {data.get("category_id")} is not found in database'},400
        course.categoy_id = data.get('category_id')
    
    if data.get('course_name') != None:
        if data.get('course_name') != course.course_name:
            exist_name= Course.get_course_by_name(data.get('course_name'))
            if exist_name != None:
                return {'msg':'course_name already used'},400
            course.course_name = data.get('course_name')
    
    course.save()
    return {'msg':'update sucessfull',
            'data':course.as_dict()
            },200

def switch_active(id):
    course = Course.get_course_by_id(id)
    course.is_active = not course.is_active
    course.save()
    return course.as_dict()
    # return {'msg': f'active status switched from {not course.is_active} to {course.is_active}. '},200