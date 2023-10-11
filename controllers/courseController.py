from flask import abort, request
from models import Course,Category
from flask_jwt_extended import current_user
from helpers.utils import checkField


def get(id):
    course=Course.get_course_by_id(id)
    result= course.as_dict()
    result['prerequisites']=[pre.as_dict() for pre in course.prerequisites]
    result['category']=course.category.category_name
    result['enrolled_users']=[{'username':enroll.user.username,
                               'status':'completed' if enroll.is_completed is True else 'uncompleted'
                               }
                               for enroll in course.enrolls]
    return result,200

def get_all():
    select= request.args.get('select','all')
    if select.lower() == 'inactive':  
        courses=Course.get_all_with_active_status(False)
    elif select.lower() == 'active':
        courses=Course.get_all_with_active_status(True)
    else :  
        courses=Course.get_all()
    # courses= [course.as_dict() for course in courses]
    # courses= [course['prerequisites'] for course in courses]
    result= []
    for c in courses:
        course= c.as_dict()
        course['prerequisites']=[]
        for p in c.prerequisites:
            course['prerequisites'].append(p.course_name)
        result.append(course)
    return {'courses':result},200

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
    
    if data.get('prerequisites')!=None:
        if isinstance(data.get('prerequisites'), list):
           for id in data.get('prerequisites'):
               pre_course= Course.get_course_by_id(id)
               if pre_course == None:
                   return {'msg':f'course id {id} not valid.'},400
               course.prerequisites.append(pre_course)
        else:
            pre_course= Course.get_course_by_id(id)
            if pre_course == None:
                return {'msg':f'course id {id} not valid.'},400
            course.prerequisites.append(pre_course)
        
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
    
    if data.get('prerequisites')!=None:
        course.prerequisites=[]
        if isinstance(data.get('prerequisites'), list):
           for id in data.get('prerequisites'):
               if id == course.course_id:
                   return {'msg':f"Can not reference to itself"},400
               pre_course= Course.get_course_by_id(id)
               if pre_course == None:
                   return {'msg':f'course id {id} not valid.'},400
               course.prerequisites.append(pre_course)
        else:
            if data.get('prerequisites')== course.course_id:
                return {'msg':f"Can not reference to itself"},400
            pre_course= Course.get_course_by_id(data.get('prerequisites'))
            if pre_course == None:
                return {'msg':f'course id {id} not valid.'},400
            course.prerequisites.append(pre_course)
    
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

def getTopCourses(numbers=5):
    enrolls= Course.get_top_favorite(numbers)
    return {'top':[dict(c) for c in enrolls]}


def searchCourseByName(course_name):
    courses=Course.query.filter_by(course_name=course_name).all()
    return {'courses':[course.as_dict() for course in courses]}

def searchCourseBypreRequisite():
    prerequisite_ids=request.get_json().get('prerequisites')
    print(prerequisite_ids)
    courses=Course.query
    # courses= Course.query.filter(Course.prerequisites.contains(Course.course_id.in_(prerequisite_ids))).all()
    if prerequisite_ids != None:
        for id in prerequisite_ids:
            print(id)
            # courses=courses.filter(Course.prerequisites.any(Course.course_id.in_([id])))
            courses=courses.filter(Course.prerequisites.any(Course.course_id.in_([id])))

    courses=courses.all()
    print(courses)
    return {'courses':[course.as_dict() for course in courses]}

def searchCourseByDescription():
    description=request.get_json().get('description')
    if description == None:
        abort(400)
    courses =Course.query.filter(Course.description.ilike(f'%{description}%'))

    return {'courses':[course.as_dict() for course in courses]}

