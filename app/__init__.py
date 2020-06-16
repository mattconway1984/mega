import flask
import flask_login
import flask_migrate
import flask_sqlalchemy

from config import Config

# Global instance of the app
app = flask.Flask(__name__)
app.config.from_object(Config)
db = flask_sqlalchemy.SQLAlchemy(app)
migrate = flask_migrate.Migrate(app, db)

# Configure the "Flask login manager"
login = flask_login.LoginManager(app)
login.login_view = "auth.login"

# Register the different parts of the application
from app.errors import bp as errors_bp
from app.auth import bp as auth_bp
from app.main import bp as main_bp
app.register_blueprint(errors_bp)
app.register_blueprint(auth_bp, url_prefix="/auth")
app.register_blueprint(main_bp)

from app import logger, models
