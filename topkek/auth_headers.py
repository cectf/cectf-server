
from flask import session
from flask_jwt import jwt_required, current_identity


def admin_jwt_required(func):
    func = jwt_required(func)

    def wrapper(*args, **kwargs):
        print("ADMIN IS REQUIRED")
        print(args)
        print(kwargs)
        print(current_identity)
        return jwt_required()(func(*args, **kwargs))
    return wrapper


def app_jwt_required(func):

    def wrapper(*args, **kwargs):
        print("APP IS REQUIRED")
        print(args)
        print(kwargs)
        print(current_identity)
        return_val = jwt_required()(func(*args, **kwargs))
        print(current_identity)
        return return_val
    return wrapper
