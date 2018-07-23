from . import auth
from app import db
from app.models.User import User
from app.email import send_email
# from utils import log
from flask_dance.contrib.google import google
from flask_dance.contrib.facebook import facebook
from ..models.Roleomg import Role
from flask import (render_template,
                   redirect,
                   request,
                   url_for,
                   flash,
                   session)
from flask_login import (login_user,
                         logout_user,
                         login_required,
                         current_user, )
from .forms import (LoginForm,
                    RegistrationForm,
                    PasswordResetForm,
                    PasswordResetRequestForm,
                    )


@auth.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.ping()
        if not current_user.confirmed \
                and request.endpoint \
                and request.blueprint != 'auth' \
                and request.endpoint != 'static':
            return redirect(url_for('auth.unconfirmed'))


@auth.route('/unconfirmed')
# is_anonymous - Must always return False for regular users.
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('main.index'))
    return render_template('auth/login/unconfirmed.html')


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            next = request.args.get('next')
            if next is None or not next.startswith('/'):
                next = url_for('main.index')
            return redirect(next)
        flash('Invalid username or password.')
    return render_template('auth/login/login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    session.clear()
    flash('You have been logged out.')
    return redirect(url_for('main.index'))


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data,
                    login_type='website')
        db.session.add(user)
        db.session.commit()
        token = user.generate_confirmation_token()
        send_email(user.email, 'Confirm Your Account',
                   'auth/email/confirm', user=user, token=token)
        flash('A confirmation email has been sent to you by email, please check your mail')
        return redirect(url_for('auth.login'))
    return render_template('auth/login/register.html', form=form)


@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    if current_user.confirm(token):
        db.session.commit()
        flash('You have confirmed your account. Thanks!')
    else:
        flash('The confirmation link is invalid or has expired.')
    return redirect(url_for('main.index'))


@auth.route('/confirm')
@login_required
def resend_confirmation():
    token = current_user.generate_confirmation_token()
    send_email(current_user.email, 'Confirm Your Account',
               'auth/email/confirm', user=current_user, token=token)
    flash('A new confirmation email has been sent to you by email.')
    return redirect(url_for('main.index'))


@auth.route('/reset', methods=['GET', 'POST'])
def password_reset_request():
    if not current_user.is_anonymous:
        return redirect(url_for('main.index'))
    form = PasswordResetRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        # log("check whether it works", user)
        if user:
            token = user.generate_reset_token()
            send_email(user.email, 'Reset Your Password',
                       'auth/email/reset_password',
                       user=user, token=token,
                       next=request.args.get('next'))
        flash('An email with instructions to reset your password has been '
              'sent to you.')
        # here need to add a page
        return redirect(url_for('auth.login'))
    return render_template('auth/login/forgot.html', form=form)


@auth.route('/reset/<token>', methods=['GET', 'POST'])
def password_reset(token):
    if not current_user.is_anonymous:
        return redirect(url_for('main.index'))
    form = PasswordResetForm()
    if form.validate_on_submit():
        if User.reset_password(token, form.new_password1.data):
            db.session.commit()
            flash('Your password has been updated.')
            return redirect(url_for('auth.login'))
        else:
            return redirect(url_for('main.index'))
    return render_template('auth/login/reset.html', form=form)


@auth.route("/login_with_google")
def login_with_google():
    if not google.authorized:
        return redirect(url_for("google.login"))
    # get google user information
    google_user = google.get("/plus/v1/people/me").json()
    print(google_user)
    # log("what is in resp", google_user)
    email = google_user["emails"][0]["value"]
    username = google_user['displayName']
    picture = google_user['image']['url']
    picture_resized = picture.split("?sz=50")[0] + "?sz=" + "512"
    role_id = Role.query.filter_by(name='user').first().id
    confirmed = True
    login_type = 'google'
    user = User(email=email, username=username, confirmed=confirmed,
                photo=picture_resized, login_type=login_type, role_id=role_id)

    user_now = User.query.filter_by(username=username).first()

    # add google user information to Database
    if user_now is None:
        db.session.add(user)
        db.session.commit()
        # log("what the type of db.session", type(db.session))
        # log("what is db session", db.session)

    user1 = User.query.filter_by(username=username).first()
    login_user(user1)
    next = request.args.get('next')
    if next is None or not next.startswith('/'):
        next = url_for('main.index')
    return redirect(next)


@auth.route("/login_with_facebook")
def login_with_facebook():
    if not facebook.authorized:
        return redirect(url_for("facebook.login"))
    facebook_user = facebook.get('me?fields=id, name, picture.width(512).height(512)').json()
    # facebook_picture = facebook.get('/me/picture?width=180&height=180').json()
    # log("test1", facebook_picture)

    facebook_id = facebook_user['id']
    username = facebook_user['name']
    picture = facebook_user['picture']['data']['url']
    email = 'M'+ facebook_user['id']
    login_type = 'facebook'
    role_id = Role.query.filter_by(name='user').first().id
    confirmed = True
    user = User(facebook_id=facebook_id, username=username, confirmed=confirmed,
                photo=picture, email=email, login_type=login_type, role_id=role_id)

    user_now = User.query.filter_by(username=username).first()

    if user_now is None:
        db.session.add(user)
        db.session.commit()

    user1 = User.query.filter_by(username=username).first()
    login_user(user1)
    next = request.args.get('next')
    if next is None or not next.startswith('/'):
        next = url_for('main.index')
    return redirect(next)

# @auth.route('/collection', method=['GET','POST'])
# def collection_list():
#     data = db.session.query(user.id,school.roll_number,)
