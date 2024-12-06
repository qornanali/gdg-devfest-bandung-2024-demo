from flask import Flask
from flask_cors import CORS
from config import Config
from middlewares.error import handle_thrown_error
from middlewares.logging import log_req_resp
from controllers.session_controller import create_session
from controllers.chat_controller import generate_chat

app = Flask(__name__)
app.config.from_object(Config)

# Enable CORS
CORS(app, resources={r"/*": {"origins": Config.ORIGIN_URL}}, supports_credentials=True)

# Middlewares
log_req_resp(app)
handle_thrown_error(app)

# Routes
@app.route("/ping", methods=["GET"])
def ping():
    return {"success": True}, 201

@app.route("/v1/sessions", methods=["POST"])
def session_route():
    return create_session()

@app.route("/v1/chat", methods=["POST"])
def chat_route():
    return generate_chat()

if __name__ == "__main__":
    app.run(port=Config.PORT, debug=Config.NODE_ENV != "production")
