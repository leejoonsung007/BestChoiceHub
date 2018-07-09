from .. import db
from . import main
import geocoder
from ..correction.name_correction import correction
from ..models.User import User
from ..models.School import School
from ..models.Pro2015 import Pro2015
from ..models.Pro2016 import Pro2016
from ..models.Pro2017 import Pro2017
from ..models.School_rank import Rank2017
from ..models.Rank import Rank
from flask import (render_template,
                   abort,
                   current_app,
                   request, redirect,
                   url_for,
                   flash,
                   jsonify, )  # json conversion
from flask_login import (login_required,
                         current_user, )
from .forms import SearchForm


@main.route('/', methods=['GET', 'POST'])
def index():
    # get user current geolocation by IP address
    loc = geocoder.ip('me')

    # search engine
    form = SearchForm()
    if form.validate_on_submit():
        input = correction(form.search.data)
        like = '%' + input + '%'
        return redirect(url_for('.result', like=like))

    # get json from front-end via Ajax
    data = request.get_json()
    if data is not None:
        school_collections = School.query.filter_by(county='Dublin')
        print(data['city'])
        first_distance_record = School.distance_calculator(float(school_collections[0].lat),
                                                           float(school_collections[0].lng),
                                                           data['lat'], data['lng'])

        # if the records exit, no need to compute the distance again
        if school_collections[0].distance == round(first_distance_record, 3):
            # print("very good")
            pass
        else:
            # add distance to database
            for school in school_collections:
                distance_computing = School.distance_calculator(float(school.lat), float(school.lng),
                                                                data['lat'], data['lng'])
                school.distance = round(distance_computing, 3)
                db.session.commit()

        page = request.args.get('page', 1, type=int)
        # schools = School.query.filter_by(county='Dublin').order_by(School.distance)
        schools = db.session.query(School.roll_number, School.official_school_name, School.website, School.email,
                                   School.deis, School.county, School.address1, School.eircode, School.fee,
                                   School.gaeltacht_area_location, School.address2, School.address3, School.address4,
                                   School.address, School.lat, School.lng, School.distance, School.total_boy,
                                   School.irish_classification, School.place_id, School.religion,
                                   School.total_girl, School.total_pupil, School.photo_ref1, School.photo_ref2,
                                   School.school_gender, School.photo_ref3, School.photo_ref4, School.photo_ref5,
                                   Pro2017.Total_progression, Rank2017.rank) \
            .outerjoin(Pro2017, School.place_id == Pro2017.place_id). \
            outerjoin(Rank2017, School.place_id == Rank2017.place_id). \
            filter(School.county == 'Dublin').order_by(School.distance)

        pagination = schools.paginate(
            page, per_page=6,
            error_out=False)
        schools_pagination = pagination.items
        return jsonify({'result': 'success', 'schools': schools_pagination})

    # pagination
    page = request.args.get('page', 1, type=int)
    # schools = School.query.filter_by(county='Dublin').order_by(School.distance)
    schools = db.session.query(School.roll_number, School.official_school_name, School.website, School.email,
                               School.deis, School.county, School.address1, School.eircode, School.fee,
                               School.gaeltacht_area_location, School.address2, School.address3, School.address4,
                               School.address, School.lat, School.lng, School.distance, School.total_boy,
                               School.irish_classification, School.place_id, School.religion,
                               School.total_girl, School.total_pupil, School.photo_ref1, School.photo_ref2,
                               School.school_gender, School.photo_ref3, School.photo_ref4, School.photo_ref5,
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
                                   School.photo_ref4, School.photo_ref5, Pro2017.Total_progression, Rank2017.rank) \
        .outerjoin(Pro2017, School.place_id == Pro2017.place_id). \
        outerjoin(Rank2017, School.place_id == Rank2017.place_id). \
        filter(School.county == 'Dublin').order_by(School.distance)

    result1 = join_search.filter(School.address.ilike(like)).all()
    result2 = join_search.filter(School.official_school_name.ilike(like)).all()

    if len(result1) != 0:
        return render_template('/main/search_result.html', school_result=result1)
    else:
        return render_template('/main/search_result.html', school_result=result2)


@main.route('/school/<official_school_name>/<roll_number>')
def school_detail(roll_number, official_school_name):
    school = School.query.filter_by(roll_number=roll_number).first()
    university_going_a=0
    university_going_b=0
    university_going_c=0
    university_only_a=0
    university_only_b=0
    university_only_c=0
    if school is not None:
        school.add += 1
        db.session.commit()

    name_list = []
    if not current_user.is_anonymous:
        comparison_list = current_user.compared.all()
        for school_ in comparison_list:
            comparison_school = School.query.filter_by(place_id=school_.compared_id).first()
            name_list.append(comparison_school.official_school_name)

    university_going2015 = Pro2015.query.filter_by(name2=official_school_name).first()
    university_going2016 = Pro2016.query.filter_by(name2=official_school_name).first()
    university_going2017 = Pro2017.query.filter_by(name2=official_school_name).first()
    universities = ['UCD', 'TCD', 'DCU', 'UCC', 'UL', 'Maynooth University', 'NUIG']
    if school is None:
        abort(404)
    return render_template('main/school_detail.html', school=school, university_going=university_going2015,
                           university_going1=university_going2016, university_going2=university_going2017,
                           universities=universities, school_names = name_list,university_going_a=university_going_a,
                           university_going_b=university_going_b, university_going_c=university_going_c,
                           university_only_a=university_only_a, university_only_b=university_only_b,
                           university_only_c=university_only_c)


@main.route('/rank', methods=['GET', 'POST'])
def rank():
    page = request.args.get('page', 1, type=int)
    # schools = db.session.query(School.roll_number, School.official_school_name, School.address, School.fee,
    #                            School.total_boy, School.total_girl, School.photo_ref1, Rank2017.p_rank, Rank2017.name,
    #                            Rank2017.rank, Rank2017.at_third_level, Rank2017.at_university,
    #                            Rank2017.stu_tea_ratio).join(Rank2017, School.place_id == Rank2017.place_id).order_by(
    #     Rank2017.rank)
    schools = db.session.query(Rank.rank, Rank.name, Rank.p_rank, Rank.photo, Rank.boy, Rank.gender_type, Rank.girl, Rank.stu_tea_ratio, Rank.at_third_level, Rank.at_university).order_by(Rank.rank)
    pagination = schools.paginate(
        page, per_page=6,
        error_out=False)
    schools_pagination = pagination.items
    # print(schools_pagination)
    return render_template('main/rank.html', pagination=pagination, schools=schools_pagination)





