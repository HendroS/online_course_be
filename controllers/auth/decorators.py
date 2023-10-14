from functools import wraps
from flask_jwt_extended import get_jwt, verify_jwt_in_request

def admin_required():
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()

            if claims["role"] !='admin':
                return {'msg':'Admins only!'}, 403
            
            return fn(*args, **kwargs)       
            
        return decorator
    
    return wrapper

def member_required():
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()

            if claims["role"] !='member':
                return {'msg':'Member only!'}, 403
            
            return fn(*args, **kwargs)       
            
        return decorator
    
    return wrapper