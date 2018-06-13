from app import db
from datetime import datetime


class Follow(db.Model):
    __tablename__ = 'follow'
    follower_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)     # 代表关注者,与relationship的follower对应
    followed_id = db.Column(db.String(50), db.ForeignKey('school.roll_number'), primary_key=True)     # 代表被关注者,与relationship的followed对应
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)


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