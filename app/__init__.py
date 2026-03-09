from flask import Flask
from .routes import main_bp
from .db_commands import register_db_commands

def create_app():
    app = Flask(__name__)

    app.register_blueprint(main_bp)
    register_db_commands(app)

    return app