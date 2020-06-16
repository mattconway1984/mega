from app import db, migrate, login
from app.models import User, Post
from app.factory import create_app

app = create_app(db, migrate, login)

@app.shell_context_processor
def make_shell_context():
    # when running `flask shell` these are automatically imported...
    return {
        "db": db,
        "User": User,
        "Post": Post,
    }
