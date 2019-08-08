from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from flask_blog import db, bcrypt
from flask_blog.models import User, Post
from flask_blog.users.forms import (RegistrationForm, LoginForm, UpdateAccountForm,
                                   RequestResetForm, ResetPasswordForm)
from flask_blog.users.utils import save_picture, send_reset_email
users= Blueprint('users',__name__)


@users.route('/register', methods=['GET', 'POST'])
def register():

    if current_user.is_authenticated:
        return redirect(url_for('main.home_page'))

    form = RegistrationForm()
    # return 'something happened here'
    # return render_template('home.html', posts=posts)
    if form.validate_on_submit():

        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode('utf8')
        user = User(username=form.username.data,
                    email=form.email.data, password=hashed_password)

        db.session.add(user)
        db.session.commit()

        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('users.login'))

    return render_template('register.html', title='Register', form=form)


@users.route('/login', methods=["GET", "POST"])
def login():

    if current_user.is_authenticated:
        return redirect(url_for('main.home_page'))

    form = LoginForm()

    if form.validate_on_submit():

        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)

            # jump to the attempted page(if any) before logged in
            # using get method otherwise it would raise a error when a query with dict key from a dict is not exist
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.home_page'))

        else:  # could remove this unrelated else branch

            flash('Login Unsuccessful, Please check email and password', 'danger')

    return render_template('login.html', title='Login', form=form)


@users.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.home_page'))


@users.route('/account', methods=['GET', 'POST'])
@login_required
def account():

    form = UpdateAccountForm()
    if form.validate_on_submit():

        if form.picture.data:

            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file

        current_user.username = form.username.data
        current_user.email = form.email.data
        # taking care updates in the db automatically with current_user and sqlalchemy
        db.session.commit()
        flash('Your account has been updated', 'success')
        # redirecting here to avoid reloading page with meanless get/post operations
        return redirect(url_for('users.account'))

    elif request.method == 'GET':
        # default value for username and email in the form
        form.username.data = current_user.username

        form.email.data = current_user.email

    image_file = url_for(
        'static', filename="profile_pics/"+current_user.image_file)

    return render_template('account.html', title='Account', image_file=image_file, form=form)


@users.route('/user/<string:username>')
def user_posts(username):

    page = request.args.get('page', 1, type=int)

    user = User.query.filter_by(username=username).first_or_404()

    post_per_page = 1

    # posts = Post.query.all()
    posts = Post.query.filter_by(author=user).order_by(Post.date_posted.desc()).paginate(
        page=page, per_page=post_per_page)
    # not showing up all the posts, paginate posts

    return render_template('user_posts.html', posts=posts, user=user)


@users.route("/reset_password", methods=['GET', 'Post'])
def reset_request():

    if current_user.is_authenticated:
        return redirect(url_for('main.home_page'))

    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password', 'info')
        return redirect(url_for('users.login'))

    return render_template('reset_request.html', title="Reset Password", form=form)


@users.route("/reset_password/<token>", methods=['GET', 'Post'])
def reset_token(token):

    if current_user.is_authenticated:
        return redirect(url_for('main.home_page'))

    user = User.verify_reset_token(token)

    if user is None:

        flash('That is an invalid or expired token', 'warning')

        return redirect(url_for('users.reset_request'))

    form = ResetPasswordForm()
    if form.validate_on_submit():

        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode('utf8')

        user.password = hashed_password
        db.session.commit()

        flash('Your password has been updated! You are now able to log in', 'success')
        return redirect(url_for('users.login'))

    return render_template('reset_token.html', title="Reset Password", form=form)
