import flask
import flask_login
import werkzeug

from app import app, db
from app.auth import bp
from app.auth.forms import (
    LoginForm,
    RegistrationForm
)
from app.models import User


@bp.route("/login", methods=["GET", "POST"])
def login():
    if flask_login.current_user.is_authenticated:
        return flask.redirect(flask.url_for("main.index"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flask.flash("Invalid username or password")
            return flask.redirect(flask.url_for("auth.login"))
        flask_login.login_user(user, remember=form.remember_me.data)
        # If the user was forced to login because they wanted to view a protected page, redirect them to that page:
        next_page = flask.request.args.get("next")
        # Note: ensure the redirect stays within the same site as the application (that's what `url_parse` does).
        if not next_page or werkzeug.urls.url_parse(next_page).netloc != "":
            next_page = flask.url_for("main.index")
        return flask.redirect(next_page)
    return flask.render_template("auth/login.html", title="Sign In", form=form)


@bp.route("/logout")
def logout():
    flask_login.logout_user()
    return flask.redirect(flask.url_for("main.index"))


@bp.route("/register", methods=["GET", "POST"])
def register():
    if flask_login.current_user.is_authenticated:
        return flask.redirect(flask.url_for("main.index"))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flask.flash("Congratulations, you are now a registered user!")
        return flask.redirect(flask.url_for("auth.login"))
    else:
        print("error")
    return flask.render_template("auth/register.html", title="Register", form=form)
