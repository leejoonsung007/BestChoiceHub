from app import db
import googlemaps
import mpu
from app.models.User_operation import Follow


class School(db.Model):
    _tablename_ = 'school'
    # __searchable__ = ['roll_number', 'official_school_name', 'county']
    place_id = db.Column(db.String(50), primary_key=True)

    roll_number = db.Column(db.String(50))
    official_school_name = db.Column(db.String(255), nullable=False)
    website = db.Column(db.String(255))
    address1 = db.Column(db.String(50))
    address2 = db.Column(db.String(50))
    address3 = db.Column(db.String(50))
    address4 = db.Column(db.String(50))
    address = db.Column(db.String(255))
    county = db.Column(db.String(50))
    eircode = db.Column(db.String(50))
    phone = db.Column(db.String(50))
    email = db.Column(db.String(50))
    principal_name = db.Column(db.String(50))
    deis = db.Column(db.String(50))
    school_gender = db.Column(db.String(50))
    pupil_attendance_type = db.Column(db.String(50))
    irish_classification = db.Column(db.String(50))
    gaeltacht_area_location = db.Column(db.String(50))
    fee = db.Column(db.String(50))
    religion = db.Column(db.String(50))
    open_close_status = db.Column(db.String(50))
    total_girl = db.Column(db.Integer)
    total_boy = db.Column(db.Integer)
    total_pupil = db.Column(db.Integer)
    lat = db.Column(db.DECIMAL(10, 6))
    lng = db.Column(db.DECIMAL(10, 6))
    # coordinate = db.Column(db.String(50))
    photo_ref1 = db.Column(db.String(255))
    photo_ref2 = db.Column(db.String(255))
    photo_ref3 = db.Column(db.String(255))
    photo_ref4 = db.Column(db.String(255))
    photo_ref5 = db.Column(db.String(255))
    distance = db.Column(db.Float(50))
    add = db.Column(db.Integer) #add school into own list, and the access+1

    followers = db.relationship('Follow',
                               foreign_keys=[Follow.followed_id],
                               backref=db.backref('followed,lazy=joined'),  # corresponding followed_id
                               lazy='dynamic',
                               cascade='all, delete-orphan')

    # userlike = db.relationship('User_like', backref=db.backref('roll_number1'), lazy='dynamic')
    # history = db.relationship('History', backref=db.backref('roll_number2'), lazy='dynamic')
    # comments = db.relationship('Comments', backref=db.backref('roll_number3'), lazy='dynamic')
    pro2015 = db.relationship('Pro2015', backref=db.backref('roll_number4'), lazy=True, uselist=False)
    pro2016 = db.relationship('Pro2016', backref=db.backref('roll_number5'), lazy='select', uselist=False)
    pro2017 = db.relationship('Pro2017', backref=db.backref('roll_number6'), lazy='select', uselist=False)
    rank2017 = db.relationship('Rank2017', backref=db.backref('roll_number3'), lazy='select', uselist=False)

    # @staticmethod
    # def distance_calculator(school_coordinate, user_coordinate):
    #     KEY = "AIzaSyA7iRMGo1sAtQBU8KNethym3uc_dgUh5GU"
    #     gmaps = googlemaps.Client(key=KEY)
    #     directions_result = gmaps.directions(school_coordinate,
    #                                          user_coordinate,
    #                                          mode="walking",
    #                                          )
    #     return (directions_result[0]['legs'][0]['distance']['text'])

    @staticmethod
    def distance_calculator(school_lat1,school_lng1, user_lat2,user_lng2):
        distance = mpu.haversine_distance((school_lat1, school_lng1), (user_lat2, user_lng2))
        return distance

    def is_followed_by(self, user):
        return self.followers.filter_by(
            follower_id=user.id).first() is not None

    def __repr__(self):
        return "<Model School `{}`>".format(self.official_school_name)
