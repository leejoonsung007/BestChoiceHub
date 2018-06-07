from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from flask_login import UserMixin
from . import db, login_manager
from utils import log
from datetime import datetime

#
class Permission:
    USER_LIKE = 1      # 关注school
    COMMENTS = 2    # 写comments
    COMMENTS_MANAGEMENT = 4  # 管理他人发表的评论
    POST_SCHOOL_INFORMATION = 8 #post学校信息
    SCHOOL_INFORMATION_MANAGEMENT = 16 #管理学校信息
    MODERATE = 32 # 协调者权限 - 不知是否多余 先留着
    ACCOUNT_MANAGEMENT = 64 #账号管理
    ADMINISTRATOR = 128      # 管理者权限

class Role(db.Model):
    __tablename__ = 'role'
    id = db.Column(db.Integer, primary_key=True)
    default = db.Column(db.Boolean, default=False)      # 只有一个角色的字段要设为True,其它都为False
    permissions = db.Column(db.Integer)                 # 不同角色的权限不同
    name = db.Column(db.String(50), unique=True)
    user = db.relationship('User', backref='role', lazy='dynamic')

    @staticmethod
    def insert_roles():
        # 这里应该是字典格式
        roles = {
            'User': [Permission.USER_LIKE, Permission.COMMENTS],  # 只有普通用户的default为True
            'Moderator': [Permission.USER_LIKE, Permission.COMMENTS, Permission.COMMENTS_MANAGEMENT,
                         Permission.POST_SCHOOL_INFORMATION, Permission.SCHOOL_INFORMATION_MANAGEMENT,
                         Permission.MODERATE
                         ],
            'Administrator': [Permission.USER_LIKE, Permission.COMMENTS, Permission.COMMENTS_MANAGEMENT,
                             Permission.POST_SCHOOL_INFORMATION, Permission.SCHOOL_INFORMATION_MANAGEMENT,
                             Permission.MODERATE, Permission.ACCOUNT_MANAGEMENT, Permission.ADMINISTRATOR
                              ],
        }
        # 这里你之前写的有点问题，我给改过来了
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.permissions = sum(roles[r])
            # print(role.permissions)
            if role.name == 'User':
                role.default = True
            db.session.add(role)
        db.session.commit()

    def __repr__(self):
        return '<Role %r>' % self.name


class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False, index=True)
    email = db.Column(db.String(50), unique=True, index=True, nullable=False)
    member_since = db.Column(db.DateTime, default=datetime.utcnow)  # 注册时间
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)  # 上次访问时间
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))
    password_hash = db.Column(db.String(128))
    confirmed = db.Column(db.Boolean, default=False)  # 邮箱令牌是否点击
    # member_since = db.Column(db.DateTime(), default=datetime.utcnow)
    # last_seen = db.Column(db.DateTime(), default=datetime.utcnow)

    # def to_json(self):
    #     user_json = {
    #         'url': url_for('api.get_user', id=self.id, _external=True),
    #         'username': self.username,
    #         'member_since': self.member_since,
    #         'last_seen': self.last_seen,
    #         'post_count': self.posts.count()
    #     }
    #     return user_json

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)        # 初始化父类
        if self.role is None:
            if self.email == current_app.config['FLASKY_ADMIN']:                  # 邮箱与管理者邮箱相同
                self.role = Role.query.filter_by(name='Administrator').first() # 权限为管理者
            # elif self.email == current_app.config['MODERATOR']:
            #     self.role = Role.query.filter_by(name='Moderator').first()
            else:
                self.role = Role.query.filter_by(default=True).first()       # 默认用户

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_confirmation_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.id}).decode('utf-8')

    def confirm(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        return True

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

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

