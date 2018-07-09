from flask_wtf import FlaskForm
from wtforms import (StringField,
                     PasswordField,
                     SubmitField, )
from wtforms.validators import (DataRequired,
                                Length,
                                EqualTo, )
from flask_wtf.file import FileField


class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('', validators=[DataRequired()])
    password1 = PasswordField('', validators=[
        DataRequired(), Length(6, 15)])

    password2 = PasswordField('', validators=[
        DataRequired(),
        EqualTo('password1', message='Passwords must match')])
    submit = SubmitField('Update Password')


class EditForm(FlaskForm):
    name = StringField('', validators=[
        DataRequired(), Length(4, 64)])
    location = StringField('', validators=[Length(0, 64)])
    submit = SubmitField('submit')


class ChangeAvatars(FlaskForm):
    avatar = FileField('')
    submit = SubmitField('submit')


