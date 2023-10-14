from flask import abort, request
from models import EnrollmentDetail,Enrollment,Chapter
from flask_jwt_extended import current_user
from helpers.utils import checkField


def getAll():
    details= EnrollmentDetail.get_all()
    return {"Enroll_detail":[d.as_dict() for d in details]}

def get(enrollment_id):
    data =request.get_json()
    chapter_id= data.get('chapter_id',None)
    chapter= Chapter.get_chapter(chapter_id)
    if chapter == None:
        return {'msg':'invalid chapter id'},400

    details = EnrollmentDetail.get_unique(enrollment_id,chapter_id)
    if details == None:
        abort(404)
    
    result = details.as_dict()
    result['chapter']=details.chapter.chapter_name
    return result


def create():
    data = request.get_json()

    enrollment_id= data.get('enrollment_id',None)
    chapter_id= data.get('chapter_id',None)

    enrollment= Enrollment.get(enrollment_id)
    if enrollment == None:
        return {'msg':'invalid enrollment_id'},400
    
    if current_user.user_id != enrollment.user_id:
        return {'msg':'The enrollment is not belong to you'},403
    
    chapter= Chapter.get_chapter(chapter_id)
    if chapter == None:
        return {'msg':'invalid chapter_id'},400
    
    if enrollment.course_id != chapter.course_id:
        return {'msg':'the chapter have not same course with enrollment course'},400
    
    enrollment_detail=EnrollmentDetail(enrollment_id=enrollment_id,
                                       chapter_id=chapter_id)
    
    enrollment_detail.save()
    result = enrollment_detail.as_dict()
    result['chapter']= enrollment_detail.chapter.chapter_name
    return result

def complete(enrollment_id):
    data =request.get_json()
    chapter_id= data.get('chapter_id',None)

    enrollment= Enrollment.get(enrollment_id)
    if enrollment == None:
        return {'msg':'invalid enrollment_id'},400
    
    if current_user.user_id != enrollment.user_id:
        return {'msg':'The enrollment is not belong to you'},403

    chapter= Chapter.get_chapter(chapter_id)
    if chapter == None:
        return {'msg':'invalid chapter id'},400

    details = EnrollmentDetail.get_unique(enrollment_id,chapter_id)
    if details == None:
        abort(404)
    
    if details.is_completed == True:
        return {'msg':'already completed'},400

    details.completed()
    return {'msg':'completed'}

