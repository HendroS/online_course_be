from flask import abort, request
from models import Course,Category,Instructor
from flask_jwt_extended import current_user
from helpers.utils import checkField,checkValidUUID


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
    select= request.args.get('select')
    if select != None and select.lower() == 'inactive':  
        courses=Course.get_all_with_active_status(False)
    elif select != None and select.lower() == 'all':
        courses=Course.get_all()
    else :  
        courses=Course.get_all_with_active_status(True)
    # courses= [course.as_dict() for course in courses]
    # courses= [course['prerequisites'] for course in courses]
    result= []
    for c in courses:
        course= c.as_dict()
        course['prerequisites']=[]
        course['instructors']=[]
        for p in c.prerequisites:
            course['prerequisites'].append(p.course_name)
        for i in c.instructors:
            course['instructors'].append(i.instructor_name)
        result.append(course)
    return {'courses':result},200

def create():
    data = request.get_json()
    required=['category_id','course_name','instructor_ids']
    not_present= checkField(required,data)
    if len(not_present)>0:
        return {'msg':f'field {", ".join(not_present)} are required.'},400
    
    if not checkValidUUID(data.get('category_id')):
        return {'msg':'invalid category UUID'},400
    
    category=Category.get_category_by_id(data.get('category_id'))
    if category == None:
        return {'msg': f'category_id {data.get("category_id")} is not found in database'},400
    course = Course(category_id=data.get("category_id"),
                    course_name = data.get("course_name"))
    
    if isinstance(data.get('instructor_ids'),str):
        if not checkValidUUID(data.get('instructor_id')):
            return {'msg':'invalid instructor UUID'},400
        
        instructor=Instructor.get_instructor(data.get('instructor_ids'))
        if instructor == None:
            return {'msg':f'invalid instructor_id {id}'},400
        course.instructors.append(instructor)

    elif isinstance(data.get('instructor_ids'),list):
        if len(data.get('instructor_ids'))<1:
            return {'msg':'required at least one valid instructor id'},400
        for id in data.get('instructor_ids'):
            if not checkValidUUID(id):
                return {'msg':'invalid instructor UUID'},400
            
            instructor=Instructor.get_instructor(id)
            if instructor == None:
                return {'msg':f'invalid instructor_id {id}'},400
            course.instructors.append(instructor)
            

    if data.get('description') != None:
        course.description = data.get('description')
    
    if data.get('prerequisites')!=None:
        if isinstance(data.get('prerequisites'), list):
           for id in data.get('prerequisites'):
                if not checkValidUUID(id):
                    return {'msg':'invalid prerequisites UUID'},400
                
                pre_course= Course.get_course_by_id(id)
                if pre_course == None:
                    return {'msg':f'course id {id} not valid.'},400
                course.prerequisites.append(pre_course)
        else:
            if not checkValidUUID(data.get('prerequisites')):
                return {'msg':'invalid prerequisites UUID'},400
            pre_course= Course.get_course_by_id(data.get('prerequisites'))
            if pre_course == None:
                return {'msg':f'course id {data.get("prerequisites")} not valid.'},400
            course.prerequisites.append(pre_course)
        
    course.save()
    result= course.as_dict()
    result['instructors']=[i.instructor_name for i in course.instructors]
    return result,201

def delete(id):
    course = Course.get_course_by_id(id)
    course.delete()
    return {'msg':'delete success'},200

def update(id):
    data = request.get_json()
    course =Course.query.filter_by(course_id=id).first_or_404()

    if data.get('description') != None:
        course.description = data.get('description')
    
    if data.get('category_id') != None:
        if not checkValidUUID(data.get('category_id')):
            return {'msg':'invalid category UUID'},400
        
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
                if not checkValidUUID(id):
                    return {'msg':'invalid prerequisites UUID'},400
                
                if id == course.course_id:
                   return {'msg':f"Can not reference to itself"},400
                pre_course= Course.get_course_by_id(id)
                if pre_course == None:
                    return {'msg':f'course id {id} not valid.'},400
                course.prerequisites.append(pre_course)
        else:
            if not checkValidUUID(data.get('prerequisites')):
                return {'msg':'invalid prerequisites UUID'},400
            
            if data.get('prerequisites')== course.course_id:
                return {'msg':f"Can not reference to itself"},400
            pre_course= Course.get_course_by_id(data.get('prerequisites'))
            if pre_course == None:
                return {'msg':f'course id {id} not valid.'},400
            course.prerequisites.append(pre_course)
    if data.get('instructor_ids')!=None:
        course.instructors=[]
        if isinstance(data.get('instructor_ids'),str):
            if not checkValidUUID(data.get('instructor_ids')):
                return {'msg':'invalid instructor UUID'},400
            
            instructor=Instructor.get_instructor(data.get('instructor_ids'))
            if instructor == None:
                return {'msg':f'invalid instructor_id {id}'},400
            course.instructors.append(instructor)

        elif isinstance(data.get('instructor_ids'),list):

            if len(data.get('instructor_ids'))<1:
                return {'msg':'required at least one valid instructor id'},400
            
            for id in data.get('instructor_ids'):
                if not checkValidUUID(id):
                    return {'msg':'invalid instructor UUID'},400


                instructor=Instructor.get_instructor(id)
                if instructor == None:
                    return {'msg':f'invalid instructor_id {id}'},400
                course.instructors.append(instructor)
    
    course.save()
    result= course.as_dict()
    result['instructors']=[i.instructor_name for i in course.instructors]
    return {'msg':'update sucessfull',
            'data':result
            },200



def switch_active(id):
    course = Course.get_course_by_id(id)
    if course == None:
        abort(404)
    course.is_active = not course.is_active
    course.save()
    return course.as_dict()
    # return {'msg': f'active status switched from {not course.is_active} to {course.is_active}. '},200

def getTopCourses(numbers=5):
    enrolls= Course.get_top_favorite(numbers)
    return {'top':[dict(c) for c in enrolls]}


def searchCourse():
    data=request.get_json()

    courses=Course.query

    if data.get('name',None) != None:
        courses=courses.filter(Course.course_name.ilike(f"%{data.get('name')}%"))

    if data.get('prerequisites') != None :
        for id in data.get('prerequisites'):
            if not checkValidUUID(id):
                return {'msg':'invalid instructor UUID'},400
        courses= courses.filter(Course.prerequisites.any(Course.course_id.in_(data.get('prerequisites'))))

    if data.get('description') != None :
        courses =Course.query.filter(Course.description.ilike(f'%{data.get("description")}%'))
    
    courses=courses.filter_by(is_active=True).all()

    return {'courses':[course.as_dict() for course in courses]}

