from datetime import datetime
from flask import request
from models import Category
from flask_jwt_extended import current_user
from helpers.utils import checkField 


def getAll():
    categories=Category.get_all()
    return {"categories":[category.as_dict() for category in categories]}

def get(id):
    category=Category.query.filter_by(category_id=id).first_or_404()
    return category.as_dict()
def delete(id):
    category=Category.query.filter_by(category_id=id).first_or_404()
    category.delete()
    return {"msg":"delete success"}

def create():
    data = request.get_json()
    category_exist=Category.get_category_by_name(data.get('category_name'))
    if category_exist != None:
        return {'msg':"category name already used"},400
    category= Category(category_name=data.get('category_name'),
                       description=data.get('description')
                       )
    category.save()
    return category.as_dict(),201
def update(id):
    data = request.get_json()
    category = Category.query.filter_by(category_id=id).first_or_404()
    if category.category_name != data.get('category_name'):
        category_exist=Category.get_category_by_name(data.get('category_name'))
        if category_exist != None:
            return {'msg':"category name already used"},400
        category.category_name= data.get('category_name')
    category.description = data.get('description')
    category.updated_at = datetime.utcnow()
    category.save()
    return category.as_dict(),200
    

