import os
from flask import request
from functools import wraps

authorizations = {
    'BasicAuth':{
        'type':'basic',
        'in':'header',
        'name':'Authorization'
    }
}

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        user = None
        auth = request.authorization
        if not auth:
            return {'message':'Authorization is missing.Please login with Credentials'}, 400
        if os.getenv("user") == auth.username:
            user = os.getenv("user") 
        auth_ok = False
        if user != None:
            auth_ok = os.getenv("password") == auth.password
        else:
            return {'message':'You dont have access for this API.Please contact the support'}, 400
        if auth_ok:
            return f(*args, **kwargs)
        else:
            return {'message':'Invalid Username/Password.'}, 400
    return decorated
