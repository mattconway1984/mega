import flask
import flask_login
import flask_migrate
import flask_sqlalchemy


db = flask_sqlalchemy.SQLAlchemy()
migrate = flask_migrate.Migrate()
login = flask_login.LoginManager()
login.login_view = "auth.login"
login.login_message = "Please login to access this page."

from app import models
