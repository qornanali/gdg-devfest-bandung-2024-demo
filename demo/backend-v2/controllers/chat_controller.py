import requests
from flask import request, jsonify
from constants.error_codes import ErrorCode
from config import Config

def generate_chat():
    data = request.get_json()
    message = data.get("message", "").strip()
    if not message:
        return jsonify({
            "success": False,
            "error": {
                "code": ErrorCode.FIELD_CANNOT_BE_BLANK,
                "message": "Message cannot be blank",
                "message_title": "Bad Request",
            }
        }), 400

    payload = {
        "contents": [{"role": "user", "parts": [{"text": message}]}],
        "safetySettings": [
            {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_ONLY_HIGH"},
        ],
        "generationConfig": {
            "temperature": Config.GEMINI_AI_TEMPERATURE,
            "maxOutputTokens": Config.GEMINI_AI_MAX_OUTPUT_TOKENS,
            "topP": Config.GEMINI_AI_TOP_P,
            "topK": Config.GEMINI_AI_TOP_K,
        },
    }

    try:
        response = requests.post(
            f"{Config.GEMINI_AI_BASE_URL}/v1beta/models/{Config.GEMINI_AI_MODEL_ID}:generateContent?key={Config.GEMINI_AI_API_KEY}",
            json=payload,
        )
        response.raise_for_status()
        content = response.json()["candidates"][0]["content"]["parts"][0]["text"]
        return jsonify({"success": True, "data": {"message": content, "created_time": 123}}), 200
    except Exception as e:
        return jsonify({
            "success": False,
            "error": {
                "code": ErrorCode.GEMINI_API_GENERIC_ERROR,
                "message": "There was an error generating the chat response",
                "message_title": "Internal Server Error",
            }
        }), 500
