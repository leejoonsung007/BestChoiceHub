from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from flask_login import UserMixin
from . import db, login_manager
from utils import log
from datetime import datetime
from .models import Permission


# class User_like(db.Model):
#     _tablename_ = 'user_like'
#     like_id = db.Column(db.String(50), primary_key=True)
#     time = db.Column(db.DateTime, default=datetime.now())
#     user_id = db.Column(db.String(50), db.ForeignKey('user.user_id'))
#     roll_number = db.Column(db.String(50), db.ForeignKey('school.roll_number'))
#
#
# class History(db.Model):
#     _tablename_ = 'user_history'
#     history_id = db.Column(db.String(50), primary_key=True)
#     time = db.Column(db.DateTime, default=datetime.now())
#     user_id = db.Column(db.String(50), db.ForeignKey('user.user_id'))
#     roll_number = db.Column(db.String(50), db.ForeignKey('school.roll_number'))
#
# class Write_comments(db.Model):
#     _tablename_ = 'write_comments'
#     w_id = db.Column(db.String(50), primary_key=True)
#     title = db.Column(db.Text, nullable=False)
#     time = db.Column(db.DateTime, default=datetime.now())
#     detail = db.Column(db.Text, nullable=False)
#     user_id = db.Column(db.String(50), db.ForeignKey('user.user_id'))
#     comments = db.relationship('Comments', backref=db.backref('w_id1'), lazy='select')
#
# class Comments(db.Model):
#     _tablename_ = 'user_comments'
#     comments_id = db.Column(db.String(50), primary_key=True)
#     time = db.Column(db.DateTime, default=datetime.now())
#     user_id = db.Column(db.String(50), db.ForeignKey('user.user_id'))
#     w_id = db.Column(db.String(50), db.ForeignKey('write_comments.w_id'))
#     roll_number = db.Column(db.String(50), db.ForeignKey('school.roll_number'))
#     detail = db.Column(db.Text, nullable=False)
#
# class School(db.Model):
#     _tablename_ = 'school'
#     roll_number = db.Column(db.String(50), primary_key=True)
#     name = db.Column(db.String(50), nullable=False)
#     address1 = db.Column(db.String(50))
#     address2 = db.Column(db.String(50))
#     address3 = db.Column(db.String(50))
#     address4 = db.Column(db.String(50))
#     website = db.Column(db.String(50))
#     country = db.Column(db.String(50))
#     eircode = db.Column(db.String(50))
#     phone = db.Column(db.String(50))
#     email = db.Column(db.String(50))
#     principal_name = db.Column(db.String(50))
#     deis = db.Column(db.String(50))
#     school_gender = db.Column(db.String(50))
#     pupil_attendance_type = db.Column(db.String(50))
#     classification = db.Column(db.String(50))
#     gaeltacht_area_location = db.Column(db.String(50))
#     fee = db.Column(db.String(50))
#     religion = db.Column(db.String(50))
#     open_close_status = db.Column(db.String(50))
#     total_girl = db.Column(db.Integer)
#     total_boy = db.Column(db.Integer)
#     total_pupil = db.Column(db.Integer)
#     lat = db.Column(db.DECIMAL(10,5)) #??
#     lag = db.Column(db.DECIMAL(10,5))  #??
#     photo_ref1 = db.Column(db.String(255))
#     photo_ref2 = db.Column(db.String(255))
#     photo_ref3 = db.Column(db.String(255))
#     photo_ref4 = db.Column(db.String(255))
#     photo_ref5 = db.Column(db.String(255))
#     photo_ref6 = db.Column(db.String(255))
#     photo_ref7 = db.Column(db.String(255))
#     photo_ref8 = db.Column(db.String(255))
#     photo_ref9 = db.Column(db.String(255))
#     photo_ref10 = db.Column(db.String(255))
#
#     userlike = db.relationship('User_like', backref=db.backref('roll_number1'), lazy='dynamic')
#     history = db.relationship('History', backref=db.backref('roll_number2'), lazy='dynamic')
#     comments = db.relationship('Comments', backref=db.backref('roll_number3'), lazy='dynamic')
#     pro2015 = db.relationship('Pro2015', backref=db.backref('roll_number4'), lazy='select', uselist=False)
#     rank2017 = db.relationship('Rank2017', backref=db.backref('roll_number5'), lazy='select', uselist=False)
#
# class Pro2015(db.Model):
#     roll_number = db.Column(db.String(50), db.ForeignKey('school.roll_number'), primary_key=True)
#     #roll_number = db.Column(db.String(50), db.ForeignKey('school.roll_number'))
#     name = db.Column(db.String(50), nullable=False)
#     name2 = db.Column(db.String(50))
#     Number_who_sat_Leaving_Cert_2015 = db.Column(db.Integer)
#     UCD = db.Column(db.Integer)
#     TCD = db.Column(db.Integer)
#     DCU = db.Column(db.Integer)
#     UL = db.Column(db.Integer)
#     Maynooth_University = db.Column(db.Integer)
#     NUIG = db.Column(db.Integer)
#     UCC = db.Column(db.Integer)
#     St_Angela = db.Column(db.Integer)
#     QUB = db.Column(db.Integer)
#     UU = db.Column(db.Integer)
#     Blanch_IT = db.Column(db.Integer)
#     Nat_Col_of_Irl = db.Column(db.Integer)
#     DIT = db.Column(db.Integer)
#     Tallaght_IT = db.Column(db.Integer)
#     Cork_IT = db.Column(db.Integer)
#     Dundalk_IT = db.Column(db.Integer)
#     GMIT = db.Column(db.Integer)
#     IADT = db.Column(db.Integer)
#     IT_Carlow = db.Column(db.Integer)
#     IT_Sligo = db.Column(db.Integer)
#     IT_Tralee = db.Column(db.Integer)
#     IT_Letter_kenny = db.Column(db.Integer)
#     IT_Limerick = db.Column(db.Integer)
#     WIT = db.Column(db.Integer)
#     Marino_Instit_of_Ed = db.Column(db.Integer)
#     C_of_I_College_of_Ed = db.Column(db.Integer)
#     Mary_Immac = db.Column(db.Integer)
#     NCAD = db.Column(db.Integer)
#     RCSI = db.Column(db.Integer)
#     Shannon_College_of_Hotel_Management = db.Column(db.Integer)
#     Total_who_accepted_CAOplace = db.Column(db.Integer)
#     Total_progression = db.Column(db.DECIMAL(10,2)) #?
#
# class Rank2017(db.Model):
#     roll_number = db.Column(db.String(50), db.ForeignKey('school.roll_number'), primary_key=True)
#     #roll_number = db.Column(db.String(50), db.ForeignKey('school.roll_number'))
#     name = db.Column(db.String(50), nullable=False)
#     rank = db.Column(db.Integer)
#     p_rank =db.Column(db.Integer)
#     gender_type = db.Column(db.String(50))
#     at_university = db.Column(db.DECIMAL(10,2)) #?
#     at_third_level =db.Column(db.DECIMAL(10,2))
#     boy =db.Column(db.Integer)
#     girl =db.Column(db.Integer)
#     stu_tea_ratio =db.Column(db.DECIMAL(10,2)) #?

