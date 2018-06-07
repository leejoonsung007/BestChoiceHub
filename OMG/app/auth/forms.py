from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo
from wtforms import ValidationError
from ..models import User
from utils import log
#此文件需要更改的地方

# Web表单
# StringField, PasswordField, BooleanField, SubmitField代表不同类型的输入框

class LoginForm(FlaskForm):
    # validator 代表要满足的条件
    # DataRequired（）表示一定要输入
    # 后面Email代表一点要是邮箱的正确格式
    email = StringField('Email', validators=[DataRequired(), Length(1, 64),
                                             Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log In')


class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1, 64),
                                             Email()])
    username = StringField('Username', validators=[
        DataRequired(), Length(1, 64),
        Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
               'Usernames must have only letters, numbers, dots or '
               'underscores')])

    password = PasswordField('Password', validators=[
        DataRequired(), Length(6,15),Regexp(regex="^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[$@$!%*?&])[A-Za-z\d$@$!%*?&]{6,}",message='The password is at least 8 characters, at least 1 uppercase letters, 1 lowercase letters, 1 numbers and 1 special characters.'),
        EqualTo('password2', message='Passwords must match.')])
    # 这里可以加一个正则表达式，比如必须有大小写字母必须有数字，然后长度一定要大于6位，格式模仿上面,(密码至少6个字符，至少1个大写字母，1个小写字母，1个数字和1个特殊字符)

    password2 = PasswordField('Confirm password', validators=[DataRequired()])
    submit = SubmitField('Register')

    def validate_email(self, field):
        # User.query - BaseQuery object
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered, please use another email')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already in use. please use another name')

