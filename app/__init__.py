from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from app.config import Config  # 🔹 Direct Import

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    
    # 🔹 Use the imported class object, not a string
    app.config.from_object(Config)

    CORS(app, resources={r"/*":{"origins":"*"}})
    db.init_app(app)

    # Ensure this path is correct based on your folder structure
    from app.routes.main_routes import main
    app.register_blueprint(main)

    return app