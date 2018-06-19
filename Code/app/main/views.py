from .. import db
from . import main
from ..models.User import User
from ..models.School import School
from ..models.Pro2015 import Pro2015
from flask import (render_template,
                   abort,
                   current_app,
                   request, redirect,
                   url_for,
                   flash,)
from flask_login import (login_required,
                         current_user,)
from .forms import (EditForm,
                    ChangePasswordForm,
                    ChangeAvatars)
from utils import log


# write a function to count the distance
# get current location from front-end


@main.route('/', methods=['GET', 'POST'])
def index():
    page = request.args.get('page', 1, type=int)
    log('what is current page', page)
    pagination = School.query.order_by(School.roll_number).paginate(
        page, per_page=6,
        error_out=False)
    schools= pagination.items
    log('schools',schools)
    for school in schools:
        log('schools', school)
    return render_template('main/home.html', schools=schools, pagination=pagination)


@main.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        abort(404)
    return render_template('main/user/user.html', user=user)


@main.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.name.data).first()

        if user is None:
            current_user.username = form.name.data
        else:
            flash("This name has existed")

        current_user.location = form.location.data
        db.session.add(current_user._get_current_object())
        db.session.commit()
        flash('Your profile has been updated.')
        return redirect(url_for('.user', username=current_user.username))

    form.name.data = current_user.username
    form.location.data = current_user.location
    return render_template('main/user/edit_profile.html', form=form)


@main.route('/change_avatar', methods=['GET', 'POST'])
@login_required
def change_avatar():
    form = ChangeAvatars()
    if form.validate_on_submit():
        # file object
        avatar = request.files['avatar']
        file_name = avatar.filename
        upload_folder = current_app.config['UPLOAD_FOLDER']
        allowed_extensions = ['png', 'jpg', 'jpeg', 'gif']
        file_type = file_name.rsplit('.', 1)[-1] if '.' in file_name else ''

        if file_type not in allowed_extensions:
            flash('File error.')
            return redirect(url_for('.user', username=current_user.username))

        # save in the database
        target = '{}{}.{}'.format(upload_folder, current_user.username, file_type)
        avatar.save(target)
        current_user.photo = '../../static/avatars/{}.{}'.format(current_user.username, file_type)
        db.session.add(current_user)
        db.session.commit()
        flash('Your avatar has been updated.')
        return redirect(url_for('.user', username=current_user.username))
    return render_template('main/user/change_avatar.html', form=form)


@main.route('/change_password', methods=['GET', 'POST'])
@login_required  # only login user can change password
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.old_password.data):
            current_user.password = form.password2.data
            db.session.add(current_user)
            db.session.commit()
            flash('Your password has been updated.')
            return redirect(url_for('main.index'))
        else:
            flash('Invalid password.')
    return render_template("main/user/change_password.html", form=form)


@main.route('/school/<official_school_name>')
def school_detail(official_school_name):
    school = School.query.filter_by(official_school_name=official_school_name).first()
    # university_going = Pro2015.query.filter_by(roll_number=roll_number).first()
    if school is None:
        abort(404)
    return render_template('main/detail/school_detail.html', school=school)


# @main.route('/school/<roll_number>')
# def find_school(roll_number):
#     school = School.query.filter_by(roll_number=roll_number).first()
#     if school is None:
#         abort(404)
#     return render_template('main/detail/school_detail.html', school=school)