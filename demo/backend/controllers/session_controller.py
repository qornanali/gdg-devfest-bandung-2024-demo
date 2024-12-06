import jwt
from flask import request, jsonify
from constants.error_codes import ErrorCode
from config import Config

def create_session():
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Basic "):
        return jsonify({
            "success": False,
            "error": {
                "code": ErrorCode.FIELD_CANNOT_BE_BLANK,
                "message": "Authorization is missing or invalid",
                "message_title": "Unauthorized",
            }
        }), 403

    if auth_header.split(" ")[1] != Config.CREDENTIAL_TOKEN:
        return jsonify({
            "success": False,
            "error": {
                "code": ErrorCode.INVALID_AUTHORIZATION,
                "message": "Invalid credentials",
                "message_title": "Unauthorized",
            }
        }), 403

    session_data = {"ip": request.remote_addr}
    token = jwt.encode(session_data, Config.SESSION_SECRET, algorithm="HS256")
    return jsonify({
        "success": True,
        "data": {
            "value": token,
            "expires_in": Config.SESSION_EXPIRATION,
        }
    }), 201
