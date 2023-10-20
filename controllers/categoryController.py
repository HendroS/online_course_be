from datetime import datetime
import os
from uuid import uuid4
from flask import request
from models import Category
from flask_jwt_extended import current_user
from werkzeug.utils import secure_filename
# from helpers.utils import checkField 


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
    # data = request.get_json()
    data = request.form
    category_name=data.get('category_name').strip()
    description= data.get('category_name')
    image= request.files.get('image')

    if category_name == None or category_name == '':
        return {'msg':'category_name cannot empty'}

    category_exist=Category.get_category_by_name(category_name)
    if category_exist != None:
        return {'msg':"category name already used"},400
    category= Category(category_name=category_name)
    if description != None:
        category.description= description
    if image != None:
        filename= secure_filename(f"{uuid4().hex}.{image.filename.split('.')[-1]}")
        path= os.path.join('public/uploaded_img/category',filename)
        image.save(path)
        category.image=filename

    category.save()
    return category.as_dict(),201
def update(id):
    # data = request.get_json()
    data = request.form
    category_name=data.get('category_name').strip()
    description= data.get('category_name')
    image= request.files.get('image')
    category = Category.query.filter_by(category_id=id).first_or_404()
    if category_name!= None and category_name != '' and category.category_name != category_name:
        category_exist=Category.get_category_by_name(category_name)
        if category_exist != None:
            return {'msg':"category name already used"},400
        category.category_name= category_name
    if description != None and description != '':
        category.description = description
    
    if image!= None:
        old_image= category.image
        filename= secure_filename(f"{uuid4().hex}.{image.filename.split('.')[-1]}")
        path= os.path.join('public/uploaded_img/category',filename)
        image.save(path)
        category.image=filename
        if old_image!=None:
            old_path= os.path.join('public/uploaded_img/category',old_image)
            os.unlink(old_path)
            
    category.updated_at = datetime.utcnow()
    category.save()
    return category.as_dict(),200
    

