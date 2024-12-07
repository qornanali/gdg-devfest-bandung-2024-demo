import requests
import time
from flask import request, jsonify
from constants.error_codes import ErrorCode
from config import Config
from redisvl.extensions.llmcache import SemanticCache
from redisvl.utils.vectorize.text.vertexai import VertexAITextVectorizer
from google.auth import load_credentials_from_file

credentials, project_id = load_credentials_from_file(Config.GOOGLE_CLOUD_CREDENTIALS)

vectorizer = VertexAITextVectorizer(
    model=Config.TEXT_EMBEDDING_MODEL_ID,
    api_config = {
        "project_id": project_id,
        "location": Config.GOOGLE_CLOUD_LOCATION,
        "credentials": credentials
    }
)

llm_cache = SemanticCache(
    distance_threshold= Config.BOT_ANSWER_CACHE_DISTANCE_THRESHOLD,
    ttl = Config.BOT_ANSWER_CACHE_TTL_IN_SECONDS,
    redis_url=f"redis://{Config.REDIS_HOST}:{Config.REDIS_PORT}",
    vectorizer=vectorizer
)

def generate_chat():
    start_time = time.time()
    usage_token = 0
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
    
    try:
        print("Checking cache for response.")
        cached_response = llm_cache.check(prompt=message)
        print(cached_response)
        if cached_response and len(cached_response) > 0:
            print("Cache hit: Returning cached response.")
            content = cached_response[0]["response"]
            end_time = time.time()
            elapsed_time = end_time - start_time
            print(f"API call successful! Time taken: {elapsed_time:.2f} seconds")
            return jsonify({
                "success": True,
                "data": {
                    "message": content,
                    "created_time": int(time.time()) * 1000,
                    "processed_seconds": elapsed_time,
                    "gemini_usage_token": usage_token
                }
            }), 200
    except Exception as e:
        print(f"Redis error during cache lookup: {e}")
    
    payload = {
        "contents": [{"role": "user", "parts": [{"text": message}]}],
        "safetySettings": [
            {
                "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                "threshold": "BLOCK_ONLY_HIGH"
            },
            {
                "category": "HARM_CATEGORY_HATE_SPEECH",
                "threshold": "BLOCK_ONLY_HIGH"
            },
            {
                "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                "threshold": "BLOCK_ONLY_HIGH"
            },
            {
                "category": "HARM_CATEGORY_HARASSMENT",
                "threshold": "BLOCK_ONLY_HIGH"
            },
        ],
        "generationConfig": {
            "temperature": Config.GEMINI_AI_TEMPERATURE,
            # "maxOutputTokens": Config.GEMINI_AI_MAX_OUTPUT_TOKENS,
            "topP": Config.GEMINI_AI_TOP_P,
            "topK": Config.GEMINI_AI_TOP_K,
        },
    }

    try:
        print("Making request to Gemini AI.")
        response = requests.post(
            f"{Config.GEMINI_AI_BASE_URL}/v1beta/models/{Config.GEMINI_AI_MODEL_ID}:generateContent?key={Config.GEMINI_AI_API_KEY}",
            json=payload,
        )
        response.raise_for_status()
        response_body = response.json()
        content = response_body["candidates"][0]["content"]["parts"][0]["text"]
        llm_cache.store(
            prompt=message,
            response=content
        )
        usage_token = response_body["usageMetadata"]["totalTokenCount"]
        print(f"Usage token count: {usage_token}")
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"API call successful! Time taken: {elapsed_time:.2f} seconds")
        return jsonify({
            "success": True,
            "data": {
                "message": content,
                "created_time": int(time.time()) * 1000,
                "processed_seconds": elapsed_time,
                "gemini_usage_token": usage_token
            }
        }), 200
    except Exception as e:
        print(f"Error generating chat response: {e}")
        return jsonify({
            "success": False,
            "error": {
                "code": ErrorCode.GEMINI_API_GENERIC_ERROR,
                "message": "There was an error generating the chat response",
                "message_title": "Internal Server Error",
            }
        }), 500
