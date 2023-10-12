from flask import abort, request
from models import UserChapter,User,Chapter
from flask_jwt_extended import current_user
from helpers.utils import checkField

def getAll():
    result= UserChapter.get_all()
    return {'result':[r.as_dict() for r in result]}

def get(user_id,chapter_id):
    result= UserChapter.get_unique(user_id,chapter_id)
    if result==None:
        abort(404)
    return result.as_dict()

def delete(user_id,chapter_id):
    result= UserChapter.get_unique(user_id,chapter_id)
    if result==None:
        abort(404)
    result.delete()
    return {'msg':'user chapter deleted'}

def create():
    data = request.get_json()
    required=['user_id','chapter_id']
    not_present= checkField(required,data)
    if len(not_present)>0:
        return {'msg':f'field {", ".join(not_present)} are required.'},400
    
    user = User.get_user_by_id(data.get('user_id'))
    if user == None:
        return {'msg':'invalid user_id'},400
    
    chapter = Chapter.get_chapter(data.get('chapter_id'))
    if chapter == None:
        return {'msg':'invalid chapter id'},400
    user_chapter= UserChapter(user_id = data.get('user_id'),
                               chapter_id = data.get('chapter_id')
                                )
    user_chapter.save()
    return user_chapter.as_dict()

def complete(user_id,chapter_id):
    user_chapter=UserChapter.get_unique(user_id,chapter_id)
    if user_chapter==None:
        abort(404)
    user_chapter.delete()
    return {'msg':'completed'}


