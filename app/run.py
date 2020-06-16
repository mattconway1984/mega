from app import app, db
from app.models import User, Post

@app.shell_context_processor
def make_shell_context():
    # when running `flask shell` these are automatically imported...
    return {
        "db": db,
        "User": User,
        "Post": Post,
    }

