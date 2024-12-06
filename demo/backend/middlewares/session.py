from flask import request, jsonify
import jwt
from constants.error_codes import ErrorCode
from config import Config

def validate_session(func):
    def wrapper(*args, **kwargs):
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return jsonify({
                "success": False,
                "error": {
                    "code": ErrorCode.FIELD_CANNOT_BE_BLANK,
                    "message": "Authorization is missing or invalid",
                    "message_title": "Unauthorized",
                }
            }), 400

        session_token = auth_header.split(" ")[1]
        try:
            session_data = jwt.decode(session_token, Config.SESSION_SECRET, algorithms=["HS256"])
            if session_data.get("ip") != request.remote_addr:
                raise jwt.InvalidTokenError
            request.environ["session_data"] = session_data
            return func(*args, **kwargs)
        except jwt.ExpiredSignatureError:
            return jsonify({
                "success": False,
                "error": {
                    "code": ErrorCode.INVALID_AUTHORIZATION,
                    "message": "Session expired",
                    "message_title": "Unauthorized",
                }
            }), 403
        except jwt.InvalidTokenError:
            return jsonify({
                "success": False,
                "error": {
                    "code": ErrorCode.INVALID_AUTHORIZATION,
                    "message": "Invalid session token",
                    "message_title": "Unauthorized",
                }
            }), 403

    return wrapper
