from flask import request
from models import User

def getAll():
    users= User.query.all()
    return [{'username':user.username} for user in users],200