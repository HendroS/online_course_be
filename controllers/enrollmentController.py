from datetime import datetime
from flask import request
from models import Course,User,Enrollment
from flask_jwt_extended import current_user
from helpers.utils import checkField , checkValidUUID



def getAll():
    enrollments= Enrollment.get_all()
    return {"enrollments":[enrollment.as_dict() for enrollment in enrollments]},200

def get(id):
    enrollment= Enrollment.query.filter_by(enrollment_id=id).first_or_404()
    result = enrollment.as_dict()
    # print([e.is_completed for e in enrollment.enrollment_details])
    detail= []
    for c in enrollment.course.chapters:
        x={'chapter':c.chapter_name}
        found=False
        for d in enrollment.enrollment_details:
            if c.chapter_id == d.chapter_id:
                x['status']= 'completed' if d.is_completed == True else 'uncompleted'
                found=True
                break
        if found == False:
            x['status']='not yet open'
        detail.append(x)

    chapter_detail={
                    'finished':len(list(filter(lambda e: e.is_completed==True ,enrollment.enrollment_details))),
                    'total_chapter':len(enrollment.course.chapters),
                    'detail': detail
                    }
    result['chapters']=chapter_detail
    result['username']= enrollment.user.username
    result['course']=enrollment.course.course_name
    # result['completed_chapter']=f"{len(enrollment.enrollment_details)} of {len(enrollment.course.chapters)}"
    return result

def delete(id):
    enrollment= Enrollment.query.filter_by(enrollment_id=id).first_or_404()
    enrollment.delete()
    return {'msg':f'success delete'},200

def create():
    max_enroll= 5
    data=request.get_json()
    #nanti ambil dari jwt
    # user=User.get_user_by_id(data.get('user_id'))
    #dari jwt
    user=current_user

    uncompleted_enroll=list(filter(lambda enroll: enroll.is_completed == False ,user.enrolls))
    
    if len(uncompleted_enroll) >= max_enroll:
        return {'msg':f'already have {len(uncompleted_enroll)} . Maximal {max_enroll} active enrollment are allowed'},400
     
    course= Course.get_course_by_id(data.get('course_id'))
    if course is None:
        return {'msg':'course not found'},400
    if not checkValidUUID(data.get('course_id')):
        return {'msg':'not valid course_id'},400
    #check prerequisites
    completed_enroll= set(filter(lambda enroll: enroll.is_completed==True , user.enrolls))
    completed_course_id=set([c.course_id for c in completed_enroll])
    course_pre_id= set([c.course_id for c in course.prerequisites])
    if course_pre_id.issubset(completed_course_id) == False:
        return {'message':'Prerequisites not fullfilled. Please take and complete course needed'},405
    
    enroll_exist=Enrollment.get_unique(user_id=user.user_id,
                                       course_id=data.get('course_id')
                                       )
    if enroll_exist != None:
        return {'msg':f'user_id {enroll_exist.user_id} already enroll to course_id {enroll_exist.course_id} .'},400

    enrollment= Enrollment(user_id = user.user_id,
                           course_id = data.get('course_id')
                           )
    enrollment.save()
    
    return enrollment.as_dict(),201



def update(id):
    enroll = Enrollment.query.filter_by(enrollment_id=id).first_or_404()
    
    if enroll.user_id != current_user.user_id:
        return {'msg':'enrollment is not belong to you'},403
   
    if enroll.is_completed == True:
        return {'msg': 'Enrollment already completed'},200
    
    enroll.is_completed = True
    enroll.updated_at = datetime.utcnow()
    enroll.save()
    return {'msg':'Completed enrollment success'},200

