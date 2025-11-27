import datetime

SECRET_KEY = "your_secret_key_here"   # keep safe!
JWT_ALGORITHM = "HS256"
JWT_EXP_DELTA = datetime.timedelta(minutes=30)  # token expiry time

import jwt
from django.conf import settings
from datetime import datetime, timedelta

def generate_jwt(user):
    payload = {
        "user_id": user.id,
        "email": user.email,
        "exp": datetime.utcnow() + JWT_EXP_DELTA,
        "iat": datetime.utcnow(),
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=JWT_ALGORITHM)
    return token

def decode_jwt(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[JWT_ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        return None   
    except jwt.InvalidTokenError:
        return None  
