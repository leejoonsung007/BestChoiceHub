from .. import db
from . import main
import geocoder
from ..models.User import User
from ..models.School import School
from ..models.Pro2015 import Pro2015
from ..models.Pro2016 import Pro2016
from ..models.Pro2017 import Pro2017
from ..models.School_rank import Rank2017
from flask import (render_template,
                   abort,
                   current_app,
                   request, redirect,
                   url_for,
                   flash,
                   jsonify, )  # json conversion
from flask_login import (login_required,
                         current_user, )
from .forms import (EditForm,
                    ChangePasswordForm,
                    ChangeAvatars,
                    SearchForm)


@main.route('/', methods=['GET', 'POST'])
def index():
    # get user current geolocation by IP address
    loc = geocoder.ip('me')

    # search engine
    form = SearchForm()
    if form.validate_on_submit():
        input = form.search.data
        like = '%' + input + '%'
        return redirect(url_for('.result', like=like))

    # get json from front-end via Ajax
    data = request.get_json()
    print(data)
    if data is not None:
        return jsonify({'BestChoice': 'we have got your location '})

    school_collections = School.query.filter_by(county='Dublin')
    first_distance_record = School.distance_calculator(float(school_collections[0].lat),
                                                       float(school_collections[0].lng),
                                                       loc.latlng[0], loc.latlng[1])

    # if the records exit, no need to compute the distance again
    if school_collections[0].distance == round(first_distance_record, 3):
        # print("very good")
        pass
    else:
        # add distance to database
        for school in school_collections:
            distance_computing = School.distance_calculator(float(school.lat), float(school.lng),
                                                            loc.latlng[0], loc.latlng[1])
            school.distance = round(distance_computing, 3)
            db.session.commit()

    # pagination
    page = request.args.get('page', 1, type=int)
    # schools = School.query.filter_by(county='Dublin').order_by(School.distance)
    schools = db.session.query(School.roll_number, School.official_school_name, School.website, School.email,
                               School.deis, School.county, School.address1, School.eircode, School.fee,
                               School.gaeltacht_area_location, School.address2, School.address3, School.address4,
                               School.address, School.lat, School.lng, School.distance, School.total_boy,
                               School.irish_classification, School.place_id, School.religion,
                               School.total_girl, School.total_pupil, School.photo_ref1, School.photo_ref2,
                               School.school_gender,School.photo_ref3, School.photo_ref4, School.photo_ref5,
                               Pro2017.Total_progression, Rank2017.rank) \
        .outerjoin(Pro2017, School.place_id == Pro2017.place_id). \
        outerjoin(Rank2017, School.place_id == Rank2017.place_id). \
        filter(School.county == 'Dublin').order_by(School.distance)

    pagination = schools.paginate(
        page, per_page=6,
        error_out=False)
    schools_pagination = pagination.items

    return render_template('main/home.html', schools=schools_pagination, pagination=pagination, form=form)


@main.route('/result/<like>')
def result(like):
    join_search = db.session.query(School.roll_number, School.official_school_name, School.website, School.email,
                                   School.deis, School.county, School.address1, School.eircode, School.fee,
                                   School.gaeltacht_area_location, School.address2, School.address3, School.address4,
                                   School.address, School.lat, School.lng, School.distance, School.total_boy,
                                   School.irish_classification,
                                   School.place_id, School.religion, School.total_girl, School.total_pupil,
                                   School.photo_ref1, School.photo_ref2, School.school_gender, School.photo_ref3,
                                   School.photo_ref4,School.photo_ref5, Pro2017.Total_progression, Rank2017.rank) \
        .outerjoin(Pro2017, School.place_id == Pro2017.place_id). \
        outerjoin(Rank2017, School.place_id == Rank2017.place_id). \
        filter(School.county == 'Dublin').order_by(School.distance)

    result1 = join_search.filter(School.address.ilike(like)).all()
    result2 = join_search.filter(School.official_school_name.ilike(like)).all()

    if len(result1) != 0:
        return render_template('/main/search/search_result.html', school_result=result1)
    else:
        return render_template('/main/search/search_result.html', school_result=result2)


@main.route('/school/<official_school_name>/<roll_number>')
def school_detail(roll_number, official_school_name):

    school = School.query.filter_by(roll_number=roll_number).first()
    university_going2015 = Pro2015.query.filter_by(name2=official_school_name).first()
    university_going2016 = Pro2016.query.filter_by(name2=official_school_name).first()
    university_going2017 = Pro2016.query.filter_by(name2=official_school_name).first()
    if school is None:
        abort(404)
    return render_template('main/detail/school_detail.html', school=school, university_going=university_going2015)


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
            # flash("This name has existed")
            pass

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

@main.route('/follow/<official_school_name>', methods=['GET', 'POST'])
@login_required
def follow(official_school_name):
    school = School.query.filter_by(official_school_name=official_school_name).first()
    if school is None:
        flash('Invalid school name.')
        return redirect(url_for('.index'))
    if current_user.is_following(school):
        flash('You have already followed this school.')
        return redirect(url_for('.school_detail', official_school_name=school.official_school_name,
                                roll_number=school.roll_number))
    current_user.follow(school)
    flash('You are now following %s.' % official_school_name)
    return redirect(url_for('.school_detail', official_school_name=school.official_school_name,
                            roll_number=school.roll_number))


@main.route('/unfollow/<official_school_name>', methods=['GET', 'POST'])
@login_required
def unfollow(official_school_name):
    school = School.query.filter_by(official_school_name=official_school_name).first()
    if school is None:
        flash('Invalid school name.')
        return redirect(url_for('.index'))
    if not current_user.is_following(school):
        flash('You have not followed this school.')
        return redirect(url_for('.school_detail', official_school_name=school.official_school_name,
                                roll_number=school.roll_number))
    current_user.unfollow(school)
    flash('Cancel following %s.' % official_school_name)
    return redirect(
        url_for('.school_detail', official_school_name=school.official_school_name, roll_number=school.roll_number))


# Add following function
@main.route('/following/<username>', methods=['GET', 'POST'])
@login_required
def following(username):
    user_ = User.query.filter_by(username=username).first()
    page = request.args.get('page', 1, type=int)
    pagination = user_.followed.paginate(
        page, per_page=current_app.config['POSTS_PER_PAGE'], error_out=False)
    # school = School.query.filter_by(place_id=item.followed_id).first()
    follows = [{'school': School.query.filter_by(place_id=item.followed_id).first(), 'timestamp': item.timestamp}
               for item in pagination.items]
    # school = School.query.filter_by(place_id=user.followed).first()
    return render_template('main/user/following.html', user=user_, title='',
                           endpoint='.following', pagination=pagination,
                           follows=follows)
