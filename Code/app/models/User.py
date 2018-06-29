from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from flask_login import UserMixin
from app import db, login_manager
# from utils import log
from datetime import datetime

from app.models.User_operation import Follow
from .Roleomg import Role


class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False, index=True)
    email = db.Column(db.String(50), unique=True, index=True, nullable=False)
    member_since = db.Column(db.DateTime, default=datetime.utcnow)  # refigister time
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)  # last seen
    location = db.Column(db.String(50))
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))
    password_hash = db.Column(db.String(128))
    confirmed = db.Column(db.Boolean, default=False)
    facebook_id = db.Column(db.String(50))
    photo = db.Column(db.String(256))
    # real_avatar = db.Column(db.String(128), default=None)
    login_type = db.Column(db.String(50))
    followed = db.relationship('Follow',
                                    foreign_keys=[Follow.follower_id],
                                    backref=db.backref('follower', lazy='joined'),
                                    lazy='dynamic',cascade='all,delete-orphan')

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)  # initial
        if self.login_type == 'website':
            if self.role is None:
                if self.email == current_app.config['FLASKY_ADMIN']:  #
                    self.role = Role.query.filter_by(name='Administrator').first()  # admin
                # elif self.email == current_app.config['MODERATOR']:
                #     self.role = Role.query.filter_by(name='Moderator').first()
                else:
                    self.role = Role.query.filter_by(default=True).first()  # default user

    def is_administrator(self):
        if self.role_id == 3:
            return True

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

    def generate_reset_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'reset': self.id}).decode('utf-8')

    #
    @staticmethod
    def reset_password(token, new_password):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except:
            return False
        user = User.query.get(data.get('reset'))
        if user is None:
            return False
        user.password = new_password
        db.session.add(user)
        return True
    def ping(self):
        self.last_seen = datetime.utcnow()
        db.session.add(self)

# Add follow function
    def follow(self, school):
        if not self.is_following(school):
            f = Follow(follower_id=self.id, followed_id=school.place_id)
            db.session.add(f)
            db.session.commit()

    def unfollow(self, school):
        f = self.followed.filter_by(followed_id=school.place_id).first()
        if f is not None:
            db.session.delete(f)
            db.session.commit()

    def is_following(self,school):
        return self.followed.filter_by(followed_id=school.place_id).first() is not None

    # whether the account is confirmed
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


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
