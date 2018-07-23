from .. import db
from . import operation
from ..models.User import User
from ..models.Roleomg import Role
from ..models.School import School
from ..models.Pro2015 import Pro2015
from ..models.Pro2016 import Pro2016
from ..models.Pro2017 import Pro2017
from ..models.Rank import Rank
from flask import (render_template,
                   abort,
                   current_app,
                   request, redirect,
                   url_for,
                   flash,
                   jsonify,
                   g)  # json conversion
from flask_login import (login_required,
                         current_user, )
from .forms import (EditForm,
                    ChangePasswordForm,
                    ChangeAvatars,
                    EditProfileAdminForm,)
from ..decorators import admin_required
from ..models.Permission import Permission
from ..models.User_operation import Comment


@operation.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        abort(404)
    page = request.args.get('page', 1, type=int)
    pagination = current_user.followed.paginate(
        page, per_page=current_app.config['POSTS_PER_PAGE'], error_out=False)
    follows = [{'school': School.query.filter_by(place_id=item.followed_id).first(), 'timestamp': item.timestamp}
               for item in pagination.items]
    return render_template('/user/user.html', user=user, title='',
                           endpoint='.following', pagination=pagination,
                           follows=follows )


@operation.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.name.data).first()

        if user is None:
            current_user.username = form.name.data
        else:
            # flash("This name has existed")
            pass

        current_user.location = form.location.data
        db.session.add(current_user._get_current_object())
        db.session.commit()
        flash('Your profile has been updated.')
        return redirect(url_for('.user', username=current_user.username))

    form.name.data = current_user.username
    form.location.data = current_user.location
    return render_template('user/edit_profile.html', form=form)


@operation.route('/edit_profile/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_profile_admin(id):
    user = User.query.get_or_404(id)
    form = EditProfileAdminForm(user=user)
    if form.validate_on_submit():
        user.email = form.email.data
        user.username = form.username.data
        user.role = Role.query.get(form.role.data)
        user.location = form.location.data
        db.session.add(user)
        db.session.commit()
        # flash('The profile has been updated.')
        return redirect(url_for('.user', username=user.username))
    form.email.data = user.email
    form.username.data = user.username
    form.role.data = user.role_id
    form.location.data = user.location
    return render_template('user/edit_profile.html', form=form, user=user)


@operation.route('/change_avatar', methods=['GET', 'POST'])
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
    return render_template('user/change_avatar.html', form=form)


@operation.route('/change_password', methods=['GET', 'POST'])
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
    return render_template("user/change_password.html", form=form)


# Add following function
@operation.route('/follow/<official_school_name>', methods=['GET', 'POST'])
@login_required
def follow(official_school_name):
    school = School.query.filter_by(official_school_name=official_school_name).first()
    if school is None:
        # flash('Invalid school name.')
        return redirect(url_for('.index'))
    if current_user.is_following(school):
        flash('You have already followed this school.')
        return redirect(url_for('.school_detail', official_school_name=school.official_school_name,
                                roll_number=school.roll_number))
    if current_user.can(Permission.FOLLOW):
        current_user.follow(school)
    # flash('You are now following %s.' % official_school_name)
    return jsonify({'result': 'success', 'school_followers': school.followers.count()})


@operation.route('/unfollow/<official_school_name>', methods=['GET', 'POST'])
@login_required
def unfollow(official_school_name):
    school = School.query.filter_by(official_school_name=official_school_name).first()
    if school is None:
        # flash('Invalid school name.')
        return redirect(url_for('.index'))
    if not current_user.is_following(school):
        flash('You have not followed this school.')
        return redirect(url_for('.school_detail', official_school_name=school.official_school_name,
                                roll_number=school.roll_number))
    current_user.unfollow(school)
    return jsonify({'result': 'success', 'school_followers': school.followers.count()})


@operation.route('/add_comparison/<official_school_name>', methods=['GET', 'POST'])
def add_to_comparison_list(official_school_name):
    school = School.query.filter_by(official_school_name=official_school_name).first()
    anonymous_user = User.current_anonymous_user()

    if school is None:
        # flash('Invalid school name.')
        return redirect(url_for('.index'))

    diverse = 'True'
    increasable = 'True'
    if current_user.is_anonymous:
        if anonymous_user.is_comparing(school):
            diverse = 'False'
        else:
            if anonymous_user.compared.count() < 4:
                anonymous_user.comparison(school)
            else:
                increasable = 'False'
    else:
        if current_user.is_comparing(school):
            diverse = 'False'
        else:
            if current_user.compared.count() < 4:
                current_user.comparison(school)
            else:
                increasable = 'False'

    if current_user.is_anonymous:
        comparison_list = anonymous_user.compared.all()
    else:
        comparison_list = current_user.compared.all()

    name_list = []
    for school_ in comparison_list:
        comparison_school = School.query.filter_by(place_id=school_.compared_id).first()
        name_list.append(comparison_school.official_school_name)

    return jsonify({'result': 'success', 'comparison_list': name_list, 'increasable': increasable, 'diverse': diverse})


@operation.route('/remove_comparison/<official_school_name>', methods=['GET', 'POST'])
def remove_from_comparison_list(official_school_name):
    school = School.query.filter_by(official_school_name=official_school_name).first()
    anonymous_user = User.current_anonymous_user()
    if school is None:
        # flash('Invalid school name.')
        return redirect(url_for('.index'))

    if current_user.is_anonymous:
        if not anonymous_user.is_comparing(school):
            # flash('You have not followed this school.')
            return redirect(url_for('.school_detail', official_school_name=school.official_school_name,
                                    roll_number=school.roll_number))
        anonymous_user.remove_comparison(school)
        comparison_list = anonymous_user.compared.all()
    else:
        if not current_user.is_comparing(school):
            # flash('You have not followed this school.')
            return redirect(url_for('.school_detail', official_school_name=school.official_school_name,
                                    roll_number=school.roll_number))
        current_user.remove_comparison(school)
        comparison_list = current_user.compared.all()

    name_list1 = []
    for school_ in comparison_list:
        comparison_school = School.query.filter_by(place_id=school_.compared_id).first()
        name_list1.append(comparison_school.official_school_name)

    return jsonify({'result': 'success', 'comparison_list': name_list1})


@operation.route('/compare/clear_all', methods=['GET', 'POST'])
def remove_all():
    anonymous_user = User.current_anonymous_user()
    if current_user.is_anonymous:
        comparison_list = anonymous_user.compared.all()
    else:
        comparison_list = current_user.compared.all()
    if len(comparison_list) != 0:
        for school_ in comparison_list:
            db.session.delete(school_)
            db.session.commit()
    return jsonify({'result': 'success'})


@operation.route('/comparing/<username>', methods=['GET', 'POST'])
def in_comparison_list(username):
    user_ = User.query.filter_by(username=username).first()
    page = request.args.get('page', 1, type=int)
    pagination = user_.compared.paginate(
        page, per_page=current_app.config['POSTS_PER_PAGE'], error_out=False)
    # school = School.query.filter_by(place_id=item.followed_id).first()
    comparisons = [{'school': School.query.filter_by(place_id=item.compared_id).first(), 'timestamp': item.timestamp}
                   for item in pagination.items]
    # school = School.query.filter_by(place_id=user.followed).first()
    return render_template('user/comparing.html', user=user_, title='',
                           endpoint='.comparing', pagination=pagination,
                           follows=comparisons)


@operation.route('/compare', methods=['GET', 'POST'])
def compare():
    comparison_school_collection = []
    rank_collection = []
    progression2015_collection = []
    progression2016_collection = []
    progression2017_collection = []

    anonymous_user = User.current_anonymous_user()
    if current_user.is_anonymous:
        comparison_list = anonymous_user.compared.all()
    else:
        comparison_list = current_user.compared.all()

    for school_ in comparison_list:
        comparison_school = School.query.filter_by(place_id=school_.compared_id).first()
        comparison_school_collection.append(comparison_school)

        school_rank = Rank.query.filter_by(place_id=school_.compared_id).first()
        rank_collection.append(school_rank)

        progression2015 = Pro2015.query.filter_by(place_id=school_.compared_id).first()
        progression2015_collection.append(progression2015)

        progression2016 = Pro2016.query.filter_by(place_id=school_.compared_id).first()
        progression2016_collection.append(progression2016)

        progression2017 = Pro2017.query.filter_by(place_id=school_.compared_id).first()
        progression2017_collection.append(progression2017)

    return render_template('user/compare.html', schools=comparison_school_collection, ranks=rank_collection,
                           pro2015=progression2015_collection, pro2016=progression2016_collection,
                           pro2017=progression2017_collection)


@operation.route('/comment/<official_school_name>', methods=['GET', 'POST'])
@login_required
def comment(official_school_name):
    school = School.query.filter_by(official_school_name=official_school_name).first()
    if school is None:
        # flash('Invalid school name.')
        return redirect(url_for('.index'))
    comments = school.comments.all()
    comment_list = []
    for comment in comments:
        single_comment = comment.__dict__
        single_comment.pop('_sa_instance_state')
        comment_list.append(single_comment)
    print(comment_list)
    return jsonify({'result':'success', 'comments': comment_list})


@operation.route('/remove_comment/<official_school_name>', methods=['GET', 'POST'])
@login_required
def remove_comment(official_school_name):
    school = School.query.filter_by(official_school_name=official_school_name).first()
    if school is None:
        # flash('Invalid school name.')
        return redirect(url_for('.index'))
    if not current_user.has_commented(school):
        flash('You have not commented this school.')
        return redirect(url_for('.school_detail', official_school_name=school.official_school_name,
                                roll_number=school.roll_number))
    current_user.remove_comment(school)
    comments = school.comments
    comment_list = []
    for comment_ in comments:
        single_comment = comment_.__dict__
        single_comment.pop('_sa_instance_state')
        comment_list.append(single_comment)
    return jsonify({'result':'success', 'comments': comment_list})
