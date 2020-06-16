import flask
from app.errors import bp
from app import db


@bp.errorhandler(404)
def not_found_error(error):
    return flask.render_template("errors/404.html"), 404


@bp.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return flask.render_template("errors/500.html"), 500
