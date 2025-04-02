from flask import Flask
from app.routes import user_routes
from flask_cors import CORS
from flask_jwt_extended import JWTManager
import os

def create_app():
    app = Flask(__name__)
    app.config["JWT_SECRET_KEY"] = str(os.getenv("SECRET_KEY"))  
    jwt = JWTManager(app)
    # CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}})
    CORS(app, resources={r"/*": {"origins": "*"}})
    app.register_blueprint(user_routes.user_bp, url_prefix='/api/users')

    return app
