from datetime import datetime, timedelta, timezone
from jose import jwt
from functools import wraps
from flask import request, jsonify
import jose
import os

KEY = os.getenv("SECRET_KEY")

def encode_token(member_id): 
    payload = {
        'exp': datetime.now(timezone.utc) + timedelta(days=0,hours=1),  # token expiation time
        'iat': datetime.now(timezone.utc), #Issued at
        'sub':  str(member_id)  # id of the user logged in
    }

    token = jwt.encode(payload, KEY, algorithm='HS256')
    return token

def token_required(f):
    @wraps(f) # this decorator preserves the original function's metadata (like its name and docstring) when it's wrapped by another function.
    def decorated(*args, **kwargs):
        token = None
        # Look for the token in the Authorization header
        # also it prevents the user from accessing protected routes without a valid token
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(" ")[1] # Bearer <token> - ["Bearer", "token"]
        
            if not token:
                return jsonify({'message': 'Token is missing!'}), 401

            try:
                # Decode the token
                data = jwt.decode(token, KEY, algorithms=['HS256'])
                print(data)
                member_id = data['sub']  # Fetch the user ID
            
            # Handle token expiration and invalid token errors
            except jose.exceptions.ExpiredSignatureError:
                return jsonify({'message': 'Token has expired!'}), 401
            # handle other JWT errors
            except jose.exceptions.JWTError:
                return jsonify({'message': 'Invalid token!'}), 401

            return f(member_id, *args, **kwargs)
        else:
            return jsonify({'message': ' You must be login to access this'}), 400

    return decorated