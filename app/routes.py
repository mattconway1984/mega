import datetime
import flask
import flask_login
import werkzeug

from app import app, db
from app.forms import (
    EditProfileForm,
    EmptyForm,
    LoginForm,
    PostForm,
    RegistrationForm
)
from app.models import User, Post


@app.before_request
def before_request():
    if flask_login.current_user.is_authenticated:
        flask_login.current_user.last_seen = datetime.datetime.utcnow()
        db.session.commit()


@app.route("/", methods=["GET", "POST"])
@app.route("/index", methods=["GET", "POST"])
@flask_login.login_required
def index():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(body=form.post.data, author=flask_login.current_user)
        db.session.add(post)
        db.session.commit()
        flask.flash("Your post is now live")
        return flask.redirect(flask.url_for("index"))
    page = flask.request.args.get("page", 1, type=int)
    posts = flask_login.current_user.followed_posts().paginate(page, app.config["POSTS_PER_PAGE"], False)
    next_url = flask.url_for("index", page=posts.next_num) if posts.has_next else None
    prev_url = flask.url_for("index", page=posts.prev_num) if posts.has_prev else None
    return flask.render_template("index.html", title="Home", form=form, posts=posts.items, next_url=next_url, prev_url=prev_url)


@app.route("/login", methods=["GET", "POST"])
def login():
    if flask_login.current_user.is_authenticated:
        return flask.redirect(flask.url_for("index"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flask.flash("Invalid username or password")
            return flask.redirect(flask.url_for("login"))
        flask_login.login_user(user, remember=form.remember_me.data)
        # If the user was forced to login because they wanted to view a protected page, redirect them to that page:
        next_page = flask.request.args.get("next")
        # Note: ensure the redirect stays within the same site as the application (that's what `url_parse` does).
        if not next_page or werkzeug.urls.url_parse(next_page).netloc != "":
            next_page = flask.url_for("index")
        return flask.redirect(flask.url_for("index"))
    return flask.render_template("login.html", title="Sign In", form=form)


@app.route("/logout")
def logout():
    flask_login.logout_user()
    return flask.redirect(flask.url_for("index"))


@app.route("/register", methods=["GET", "POST"])
def register():
    if flask_login.current_user.is_authenticated:
        return flask.redirect(flask.url_for("index"))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flask.flash("Congratulations, you are now a registered user!")
        return flask.redirect(flask.url_for("login"))
    else:
        print("error")
    return flask.render_template("register.html", title="Register", form=form)


@app.route("/user/<username>")
@flask_login.login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    page = flask.request.args.get("page", 1, type=int)
    posts = user.posts.order_by(Post.timestamp.desc()).paginate(page, app.config["POSTS_PER_PAGE"], False)
    next_url = flask.url_for("user", username=user.username, page=posts.next_num) if posts.has_next else None
    prev_url = flask.url_for("user", username=user.username, page=posts.prev_num) if posts.has_prev else None
    form = EmptyForm()
    return flask.render_template("user.html", title="My Profile", user=user, posts=posts.items, next_url=next_url, prev_url=prev_url, form=form)


@app.route("/edit_profile", methods=["GET", "POST"])
@flask_login.login_required
def edit_profile():
    form = EditProfileForm(flask_login.current_user.username)
    if form.validate_on_submit():
        flask_login.current_user.username = form.username.data
        flask_login.current_user.about_me = form.about_me.data
        db.session.commit()
        flask.flash("Your changes have been saved.")
        return flask.redirect(flask.url_for("user", username=flask_login.current_user.username))
    elif flask.request.method == "GET":
        form.username.data = flask_login.current_user.username
        form.about_me.data = flask_login.current_user.about_me
    return flask.render_template(
        "edit_profile.html",
        title="Edit Profile",
        form=form)

@app.route("/follow/<username>", methods=["POST"])
@flask_login.login_required
def follow(username):
    form = EmptyForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=username).first()
        if user is None:
            flask.flash(f"User {username} not found.")
            return flask.redirect(flask.url_for("index"))
        if user == flask_login.current_user:
            flask.flash("You cannot follow yourself!")
            return flask.redirect(flask.url_for("user", username=username))
        flask_login.current_user.follow(user)
        db.session.commit()
        flask.flash(f"You're now following {username}")
        return flask.redirect(flask.url_for("user", username=username))
    else:
        return flask.redirect(flask.url_for("index"))


@app.route("/unfollow/<username>", methods=["POST"])
@flask_login.login_required
def unfollow(username):
    form = EmptyForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=username).first()
        if user is None:
            flask.flash(f"User {username} not found.")
            return flask.redirect(flask.url_for("index"))
        if user == flask_login.current_user:
            flask.flash("You cannot unfollow yourself!")
            return flask.redirect(flask.url_for("user", username=username))
        flask_login.current_user.unfollow(user)
        db.session.commit()
        flask.flash(f"You are not following {username}")
        return flask.redirect(flask.url_for("user", username=username))
    else:
        return flask.redirect(flask.url_for("index"))


@app.route("/explore")
@flask_login.login_required
def explore():
    page = flask.request.args.get("page", 1, type=int)
    posts = Post.query.order_by(Post.timestamp.desc()).paginate(page, app.config["POSTS_PER_PAGE"], False)
    next_url = flask.url_for("explore", page=posts.next_num) if posts.has_next else None
    prev_url = flask.url_for("explore", page=posts.prev_num) if posts.has_prev else None
    return flask.render_template("index.html", title="Explore", posts=posts.items, next_url=next_url, prev_url=prev_url)
