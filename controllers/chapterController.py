import os
from uuid import uuid4
from flask import abort, request
from models import Chapter,Course
from flask_jwt_extended import current_user
from helpers.utils import checkField,checkValidUUID
from werkzeug.utils import secure_filename

def getAll():
    chapters=Chapter.get_all()
    return {'chapters':[chapter.as_dict() for chapter in chapters]}

def get(id):
    chapter=Chapter.query.filter_by(chapter_id=id).first_or_404()
    return chapter.as_dict()

def delete(id):
    chapter=Chapter.query.filter_by(chapter_id=id).first_or_404()
    chapter.delete()
    return {'msg':'delete successfull'}

def softDelete(id):
    chapter=Chapter.query.filter_by(chapter_id=id).first_or_404()
    chapter.softDelete()
    return {'msg':'soft deleted'}

def create():
    # data = request.get_json()
    data = request.form
    image= request.files.get('image')
    required=['course_id','chapter_name','order','content']
    not_present= checkField(required,data)
    if len(not_present)>0:
        return {'msg':f'field {", ".join(not_present)} are required.'},400
    
    if not checkValidUUID(data.get('course_id')):
        return {'msg':'invalid course_id'},400

    course= Course.get_course_by_id(data.get('course_id'))
    if course == None:
        return {'msg':'course_id not found'},400
    
    chapter= Chapter(course_id=data.get('course_id'),
                     chapter_name=data.get('chapter_name'),
                     order=data.get('order'),
                     content=data.get('content')
                     )
    if data.get('description'):
        chapter.image=data.get('description')
    
    if image != None:
        filename= secure_filename(f"{uuid4().hex}.{image.filename.split('.')[-1]}")
        path= os.path.join('public/uploaded_img/chapter',filename)
        image.save(path)
        chapter.image= filename

    chapter.save()
    return chapter.as_dict(),201

def update(id):
    # data = request.get_json()
    data = request.form
    image= request.files.get('image')
    required=['chapter_name','order']
    not_present= checkField(required,data)
    if len(not_present)>0:
        return {'msg':f'field {", ".join(not_present)} are required.'},400
    
    chapter= Chapter.query.filter_by(chapter_id=id).first_or_404()
    
    # course= Course.get_course_by_id(data.get('course_id'))
    # if course == None:
    #     return {'msg':'invalid course_id'},400
    
    # chapter.course_id = data.get('course_id')
    chapter.name = data.get('chapter_name')
    chapter.order = data.get('order')

    if data.get('content'):
        chapter.content=data.get('content')
    
    if data.get('description'):
        chapter.description=data.get('description')

    if image!= None:
        old_image= chapter.image
        filename= secure_filename(f"{uuid4().hex}.{image.filename.split('.')[-1]}")
        path= os.path.join('public/uploaded_img/chapter',filename)
        image.save(path)
        chapter.image=filename
        if old_image!=None:
            old_path= os.path.join('public/uploaded_img/chapter',old_image)
            os.unlink(old_path)

    chapter.save()

    return chapter.as_dict()


