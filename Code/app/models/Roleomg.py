from app import db
from .Permission import Permission


class Role(db.Model):
    __tablename__ = 'role'
    id = db.Column(db.Integer, primary_key=True)
    default = db.Column(db.Boolean, default=False)  # user is set to default role- True
    permissions = db.Column(db.Integer)
    name = db.Column(db.String(50), unique=True)
    user = db.relationship('User', backref='role', lazy='dynamic')

    @staticmethod
    def insert_roles():
        roles = {
            'User': [Permission.USER_LIKE, Permission.COMMENTS],
            'Moderator': [Permission.USER_LIKE, Permission.COMMENTS, Permission.COMMENTS_MANAGEMENT,
                          Permission.POST_SCHOOL_INFORMATION, Permission.SCHOOL_INFORMATION_MANAGEMENT,
                          Permission.MODERATE
                          ],
            'Administrator': [Permission.USER_LIKE, Permission.COMMENTS, Permission.COMMENTS_MANAGEMENT,
                              Permission.POST_SCHOOL_INFORMATION, Permission.SCHOOL_INFORMATION_MANAGEMENT,
                              Permission.MODERATE, Permission.ACCOUNT_MANAGEMENT, Permission.ADMINISTRATOR
                              ],
        }
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.permissions = sum(roles[r])
            if role.name == 'User':
                role.default = True
            db.session.add(role)
        db.session.commit()

    def __repr__(self):
        return '<Role %r>' % self.name
