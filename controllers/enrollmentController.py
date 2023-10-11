from datetime import datetime
from flask import abort, jsonify, request
from models import Course,User,Enrollment
from flask_jwt_extended import current_user
from helpers.utils import checkField 



def getAll():
    enrollments= Enrollment.get_all()
    return {"enrollments":[enrollment.as_dict() for enrollment in enrollments]},200

def create():
    max_enroll= 5
    data=request.get_json()
    #nanti ambil dari jwt
    user=User.get_user_by_id(data.get('user_id'))
    if user is None:
        return {'msg':'user_id is invalid'},400
    uncompleted_enroll=list(filter(lambda enroll: enroll.is_completed == False ,user.enrolls))
    
    if len(uncompleted_enroll) >= max_enroll:
        return {'msg':f'already have {len(uncompleted_enroll)} . Maximal {max_enroll} active enrollment are allowed'},400
     
    course= Course.get_course_by_id(data.get('course_id'))
    if course is None:
        return {'msg':'course_id is invalid'},400
    if course.course_id == data.get('course_id'):
        return {'msg':"Cannot prerequisited by itself"},400
    
    enroll_exist=Enrollment.get_unique(user_id=data.get('user_id'),
                                       course_id=data.get('course_id')
                                       )
    if enroll_exist != None:
        return {'msg':f'user_id {enroll_exist.user_id} already enroll to course_id {enroll_exist.course_id} .'},400

    enrollment= Enrollment(user_id = data.get('user_id'),
                           course_id = data.get('course_id')
                           )
    enrollment.save()
    
    return enrollment.as_dict(),201

def delete(course_id):
    #nanti dari jwt
    user_id = request.get_json().get('user_id',None)
    if user_id==None:
        return {'msg':'user_id needed'},400
    enroll = Enrollment.get_unique(user_id=user_id,course_id=course_id)
    if enroll == None:
        return {'msg':'enrollment not found'},404
    print(enroll)
    enroll.delete()
    return {'msg':f'success delete {enroll}'},200

def update(course_id):
    data=request.get_json()
    #nanti ambil dari jwt
    user=User.get_user_by_id(data.get('user_id'))
    if user is None:
        return {'msg':'user_id is invalid'},400
    # uncompleted_enroll=list(filter(lambda enroll: enroll.is_completed == False ,user.enrolls))
    course= Course.get_course_by_id(course_id)
    if course is None:
        return {'msg':'course_id is invalid'},400
    
    enroll=Enrollment.get_unique(user_id=data.get('user_id'),
                                course_id=course_id
                                )
    if enroll == None:
        return {'msg': 'Enrollment not found'},404
    
    if enroll.is_completed == True:
        return {'msg': 'Enrollment already completed'},200
    
    enroll.is_completed = True
    enroll.updated_at = datetime.utcnow()
    enroll.save()
    return {'msg':'Completed enrollment success'},200

