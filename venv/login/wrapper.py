from functools import wraps
from flask import abort
import jwt

def authorize(f):
    @wraps(f)
    def decorated_function(*args, **kws):
            if not 'Authorization' in request.headers:
               abort(401)

            user = None
            data = request.headers['Authorization'].encode('ascii','ignore')
            token = str.replace(str(data), 'Bearer ','')
            try:
                user = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])['sub']
            except:
                abort(401)

            return f(user, *args, **kws)
    return decorated_function
