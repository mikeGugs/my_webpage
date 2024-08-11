from flask import Flask
from config import ProductionConfig
from app.extensions import mail
from app.extensions import db


def create_app(config_class=ProductionConfig):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize Flask extensions here
    db.init_app(app)
    mail.init_app(app)

    # Blueprints for non-auth parts of ap
    from app.main import bp as main_bp
    from app.error_handlers.errors import error

    # Blueprints for auth parts of app
    from app.auth import auth_bp as auth_blueprint

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(error)

    return app
