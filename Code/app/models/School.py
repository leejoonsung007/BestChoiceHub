from app import db
#from app.models.User_operation import Follow

class School(db.Model):
    _tablename_ = 'school'
    roll_number = db.Column(db.String(50), primary_key=True)
    official_school_name = db.Column(db.String(255), nullable=False)
    website = db.Column(db.String(255))
    address1 = db.Column(db.String(50))
    address2 = db.Column(db.String(50))
    address3 = db.Column(db.String(50))
    address4 = db.Column(db.String(50))
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
    photo_ref1 = db.Column(db.String(255))
    photo_ref2 = db.Column(db.String(255))
    photo_ref3 = db.Column(db.String(255))
    photo_ref4 = db.Column(db.String(255))
    photo_ref5 = db.Column(db.String(255))

    followed = db.relationship('Follow',  # 该用户的关注者们，对于关注者们而言，关注者们关注了该用户
                                backref=db.backref('follower'),  # 对应followed_id
                                lazy='joined',
                                cascade='all, delete-orphan')


    # userlike = db.relationship('User_like', backref=db.backref('roll_number1'), lazy='dynamic')
    # history = db.relationship('History', backref=db.backref('roll_number2'), lazy='dynamic')
    # comments = db.relationship('Comments', backref=db.backref('roll_number3'), lazy='dynamic')
    pro2015 = db.relationship('Pro2015', backref=db.backref('roll_number4'), lazy='select', uselist=False)
    pro2016 = db.relationship('Pro2016', backref=db.backref('roll_number5'), lazy='select', uselist=False)
    pro2017 = db.relationship('Pro2017', backref=db.backref('roll_number6'), lazy='select', uselist=False)
    rank2017 = db.relationship('Rank2017', backref=db.backref('roll_number5'), lazy='select', uselist=False)

    def __init__(self, name):
        self.official_school_name = name

    def __repr__(self):
        return "<Model School `{}`>".format(self.official_school_name)