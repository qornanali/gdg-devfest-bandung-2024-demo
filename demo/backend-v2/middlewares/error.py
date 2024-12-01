from flask import jsonify
from constants.error_codes import ErrorCode

def handle_thrown_error(app):
    @app.errorhandler(Exception)
    def handle_exception(e):
        app.logger.error(f"Error: {str(e)}")
        return jsonify({
            "success": False,
            "error": {
                "code": ErrorCode.GENERIC_ERROR,
                "message": "There is an unexpected error. Please try again!",
                "message_title": "Internal Server Error",
            }
        }), 500
