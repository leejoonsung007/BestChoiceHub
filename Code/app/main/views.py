from .. import db
from . import main
import requests
import json
from ..correction.name_correction import correction
from ..models.School import School
from ..models.Pro2015 import Pro2015
from ..models.Pro2016 import Pro2016
from ..models.Pro2017 import Pro2017
from ..models.Rank import Rank
from ..models.User import User
from flask import (render_template,
                   abort,
                   request, redirect,
                   url_for,
                   jsonify,
                   flash)  # json conversion
from flask_login import current_user
from .forms import SearchForm
from .forms import CommentForm
from ..models.Permission import Permission
from ..models.User_operation import Comment
import re

current_location = None


@main.route('/distance_computing/<geolocation>', methods=['GET', 'POST'])
def distance_computing(geolocation):
    # process geolocation data
    geo_split = geolocation.split(',')
    print(geo_split[0], geo_split[1])

    global current_location
    current_location = geo_split

    # count the total number of page
    url = "http://ip-api.com/json"
    geo_req = requests.get(url)
    geo_json = json.loads(geo_req.text)
    school_list = School.query.filter_by(county=geo_json['city'])
    page_count = school_list.count() // 6

    schools = db.session.query(School, Pro2017, Rank).outerjoin(Pro2017) \
        .outerjoin(Rank).filter(School.county == geo_json['city']).all()
    schools_list = list(schools)

    # compute distance for each school
    for school in schools_list:
        distance_computing = School.distance_calculator(float(school[0].lat), float(school[0].lng),
                                                        float(geo_split[0]), float(geo_split[1]))
        school = list(school)
        school[0].distance = distance_computing

    # sort the data by distance
    schools_list.sort(key=lambda x: x[0].distance)

    json_list = []
    for school in schools_list:
        dict1 = {}
        dict2 = school[0].__dict__
        dict2.pop('_sa_instance_state')
        if school[1] is not None:
            dict3 = school[1].__dict__
            dict3.pop('_sa_instance_state')
        else:
            dict3 = {'Total_progression2': 'No Data', 'Total_progression': 'No data'}
        if school[2] is not None:
            dict4 = school[2].__dict__
            dict4.pop('_sa_instance_state')
        else:
            dict4 = {'rank': 'No Data', 'p_rank': 'No data'}

        dict1.update(dict2)
        dict1.update(dict3)
        dict1.update(dict4)
        json_list.append(dict1)

    return jsonify({'result': json_list, 'page_counte': page_count})


@main.route('/', methods=['GET', 'POST'])
def index():
    if User.current_anonymous_user():
        pass
    else:
        User.create_anonymous()
    # search engine
    form = SearchForm()
    if form.validate_on_submit():
        input_ = form.search.data
        input_1 = input_.replace(' ', '')
        num = re.findall('\d+', input_1)
        if len(input_) < 10:
            if len(num) >= 1:
                input_process = input_1.split(num[0])
                input_process1 = correction(input_process[0]) + num[0]
                input_process2 = input_process1.replace(num[0], (' ' + num[0]))
            else:
                input_process2 = correction(input_)
        else:
            input_process2 = correction(input_)

        temp = []
        if form.select.data.lower() in input_process2.lower():
            input = input_process2
            temp.append(input)
        else:
            input = input_process2 + ' ' + form.select.data
            temp.append(input_process2)
            temp.append(form.select.data)

        if ',' in input:
            new_input = input.replace(',', ' ')
            input_split = new_input.split()
        elif '.' in input:
            new_input = input.replace('.', ' ')
            input_split = new_input.split()
        else:
            input_split = temp

        if len(input_split) > 1:
            like = ''
            for split in input_split:
                like += '%' + split + '%'
        else:
            like = '%' + input_split[0] + '%'

        return redirect(url_for('.result', like=like))

    return render_template('main/home.html', form=form)


@main.route('/result/<like>')
def result(like):
    print(like)
    global current_location
    if current_location is None:
        url = "http://ip-api.com/json"
        geo_req = requests.get(url)
        geo_json = json.loads(geo_req.text)
        current_location = [geo_json['lat'], geo_json['lon']]
    print(current_location)

    join_search = db.session.query(School, Rank, Pro2017).outerjoin(Rank).outerjoin(Pro2017)

    counties = ['Antrim', 'Armagh', 'Carlow', 'Cavan', 'Clare', 'Cork', 'Derry', 'Donegal', 'Down', 'Dublin',
                'Fermanagh', 'Galway', 'Kerry', 'Kildare', 'Kilkenny', 'Laois', 'Leitrim', 'Limerick',
                'Longford', 'Louth', 'Mayo', 'Meath', 'Monaghan', 'Offaly', 'Roscommon',
                'Sligo', 'Tipperary', 'Tyrone', 'Waterford', 'Westmeath', 'Wexford', 'Wicklow']

    for county in counties:
        if '%All%' in like:
            new_like1 = like.replace('%All%', '')
            result1 = join_search.filter(School.address.ilike(new_like1)).all()
            result2 = join_search.filter(School.official_school_name.ilike(new_like1)).all()
        elif '%' + county + '%' in like:
            new_like2 = like.replace('%' + county + '%', '')
            result1 = join_search.filter(School.address.ilike(like)).all()
            result2 = join_search.filter(School.official_school_name.ilike(new_like2),
                                         School.county.like('%' + county + '%')).all()
        else:
            # Dublin 4
            result1 = join_search.filter(School.address.ilike(like)).all()

    if len(result1) != 0:
        result_1 = result1
        # compute distance for each school
        for school in result_1:
            distance_computing = School.distance_calculator(float(school[0].lat), float(school[0].lng),
                                                            float(current_location[0]), float(current_location[1]))
            school = list(school)
            school[0].distance = round(distance_computing, 2)
        # sort the data by distance
        result_1.sort(key=lambda x: x[0].distance)
        return render_template('/main/filter.html', school_result=result_1)
    elif like == '%All%':
        result_3 = join_search.all()
        # compute distance for each school
        for school in result_3:
            distance_computing = School.distance_calculator(float(school[0].lat), float(school[0].lng),
                                                            float(current_location[0]), float(current_location[1]))
            school = list(school)
            school[0].distance = round(distance_computing, 2)
        # sort the data by distance
        result_3.sort(key=lambda x: x[0].distance)
        return render_template('/main/filter.html', school_result=result_3)
    else:
        result_2 = result2
        # compute distance for each school
        for school in result2:
            distance_computing = School.distance_calculator(float(school[0].lat), float(school[0].lng),
                                                            float(current_location[0]), float(current_location[1]))
            school = list(school)
            school[0].distance = round(distance_computing, 2)
        # sort the data by distance
        result_2.sort(key=lambda x: x[0].distance)
        return render_template('/main/filter.html', school_result=result_2)


@main.route('/school/<official_school_name>/<roll_number>', methods=['POST', 'GET'])
def school_detail(roll_number, official_school_name):
    if User.current_anonymous_user():
        pass
    else:
        User.create_anonymous()
    school = db.session.query(School, Rank, Pro2015, Pro2016, Pro2017).filter_by(roll_number=roll_number) \
        .outerjoin(Rank).outerjoin(Pro2015).outerjoin(Pro2016).outerjoin(Pro2017).first()

    if school is None:
        abort(404)

    # school sample
    # (< Model School `Blackrock College` >, < Rank ChIJUVrVbdAIZ0gRC3qozmRomPQ >,
    # < Model Pro2015 `Blackrock College, Blackrock, Co Dublin` >, None, < Model Pro2017 `Blackrock College` >)
    if school[0] is not None:
        school[0].add = school[0].add + 1
        db.session.commit()

    if not current_user.is_anonymous:
        comparison_list = current_user.compared.all()
    else:
        anonymous_user = User.current_anonymous_user()
        comparison_list = anonymous_user.compared.all()

    name_list = []
    for school_ in comparison_list:
        comparison_school = School.query.filter_by(place_id=school_.compared_id).first()
        name_list.append(comparison_school.official_school_name)

    universities = ['UCD', 'TCD', 'DCU', 'UCC', 'UL', 'Maynooth University', 'NUIG']

    form = CommentForm()
    current_user_info = current_user._get_current_object()
    if form.validate_on_submit() and current_user.can(Permission.COMMENT):
        if current_user.has_commented(school[0]):
            flash('your have commented this school')
        else:
            user_review = form.body.data
            if '<' or '>' in user_review:
                user_review = user_review.replace('<', '')
                user_review = user_review.replace('>', '')

            comment = Comment(author=current_user_info,
                              author_avatar=current_user_info.photo,
                              user_review=user_review, user_rating=form.rating.data,
                              commented_official_school_name=official_school_name,
                              school_id=school[0].place_id,
                              author_name=current_user_info.username)
            db.session.add(comment)
            db.session.commit()

    comments = Comment.query.filter_by(commented_official_school_name=official_school_name) \
        .order_by(Comment.time.desc())

    page = request.args.get('page', 1, type=int)
    pagination = comments.paginate(
        page, per_page=6,
        error_out=False)
    comment_pagination = pagination.items
    review_number = comments.count()

    rate_list = []
    for comment in comments:
        rate_list.append(comment.user_rating)
    overall_rate = Comment.compute_overall_rate(rate_list)

    return render_template('main/school_detail.html', school=school[0], rank=school[1],
                           university_going=school[2], university_going1=school[3], university_going2=school[4],
                           universities=universities, school_names=name_list, university_going_a=0,
                           university_going_b=0, university_going_c=0, university_only_a=0,
                           university_only_b=0, university_only_c=0, comments=comment_pagination,
                           overall_rate=overall_rate, pagination=pagination,
                           count=review_number, school_name=official_school_name, roll_number=roll_number, form=form)


@main.route('/rank', methods=['GET', 'POST'])
def rank():
    page = request.args.get('page', 1, type=int)
    schools = db.session.query(School.roll_number, School.official_school_name, School.address, School.fee,
                               School.photo_ref1, Rank.rank, Rank.name, Rank.official_school_name, Rank.p_rank,
                               Rank.boy,Rank.gender_type, Rank.girl, Rank.stu_tea_ratio, Rank.at_third_level,
                               Rank.at_university).join(Rank, School.place_id == Rank.place_id).order_by(Rank.rank)

    pagination = schools.paginate(
        page, per_page=6,
        error_out=False)
    schools_pagination = pagination.items
    return render_template('main/rank.html', pagination=pagination, schools=schools_pagination)
