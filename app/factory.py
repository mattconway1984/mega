import flask

from config import Config

from app.logger import configure_logger


def create_app(db, migrate, login, config_class=Config):
    """
    Create a new instance of the Flask application.
    """
    app = flask.Flask(__name__)
    app.config.from_object(config_class)
    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    from app.errors import bp as errors_bp
    from app.auth import bp as auth_bp
    from app.main import bp as main_bp
    app.register_blueprint(errors_bp)
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(main_bp)
    configure_logger(app)
    return app
