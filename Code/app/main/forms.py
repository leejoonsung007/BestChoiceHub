from flask_wtf import FlaskForm
from wtforms import (StringField,
                     PasswordField,
                     SubmitField, )
from wtforms.validators import (DataRequired,
                                Length,
                                Email,
                                Regexp,
                                EqualTo, )

class SearchForm(FlaskForm):
    search = StringField('', validators=[DataRequired(), Length(0, 64)])
    submit = SubmitField('submit')


