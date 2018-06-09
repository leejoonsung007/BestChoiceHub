from app import db


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