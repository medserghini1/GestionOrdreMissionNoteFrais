from functools import wraps
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from flask import jsonify

def role_required(*roles):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request()
            user = get_jwt_identity()
            if user['role'] not in roles:
                return jsonify({'msg': 'Accès refusé'}), 403
            return fn(*args, **kwargs)
        return wrapper
    return decorator