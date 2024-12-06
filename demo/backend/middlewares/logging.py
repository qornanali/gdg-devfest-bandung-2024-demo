import uuid
from flask import request

def log_req_resp(app):
    @app.before_request
    def log_request():
        request_id = request.headers.get("request-id", str(uuid.uuid4()))
        request.environ["request_id"] = request_id
        app.logger.info(f"Request ID={request_id}: {request.method} {request.path}")

    @app.after_request
    def log_response(response):
        request_id = request.environ.get("request_id")
        app.logger.info(f"Response ID={request_id}: {response.status}")
        return response
