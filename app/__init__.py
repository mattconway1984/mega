import flask
import flask_login
import flask_migrate
import flask_sqlalchemy

from config import Config

app = flask.Flask(__name__)
app.config.from_object(Config)
db = flask_sqlalchemy.SQLAlchemy(app)
migrate = flask_migrate.Migrate(app, db)

# Configure the "Flask login manager":
login = flask_login.LoginManager(app)
login.login_view = "login"

from app import logger, routes, models, errors
