from flask_wtf import FlaskForm
from wtforms import (StringField,
                     PasswordField,
                     SubmitField,
                     SelectField)
from wtforms.validators import (DataRequired,
                                Length,
                                Email,
                                Regexp,
                                EqualTo, )


class SearchForm(FlaskForm):
    search = StringField('', validators=[Length(0, 64)])
    select = SelectField('', choices=[('All', 'All'),('Dublin', 'Dublin'), ('Cork', 'Cork'), ('Galway', 'Galway'),
                                      ('Limerick', 'Limerick'), ('Antrim', 'Antrim'), ('Antrim', 'Antrim'),
                                      ('Carlow', 'Carlow'), ('Cavan', 'Cavan'), ('Clare', 'Clare'),
                                      ('Derry', 'Derry'), ('Donegal', 'Donegal'), ('Down', 'Down'),
                                      ('Fermanagh', 'Fermanagh'), ('Kerry', 'Kerry'), ('Leitrim', 'Leitrim'),
                                      ('Kilkenny', 'Kilkenny'), ('Laois', 'Laois'), ('Kildare', 'Kildare'),
                                      ('Longford', 'Longford'), ('Louth', 'Louth'), ('Mayo', 'Mayo'),
                                      ('Meath', 'Meath'), ('Monaghan', 'Monaghan'), ('Offaly', 'Offaly'),
                                      ('Roscommon', 'Roscommon'), ('Sligo', 'Sligo'), ('Tipperary', 'Tipperary'),
                                      ('Tyrone', 'Tyrone'), ('Kerry', 'Kerry'), ('Kildare', 'Kildare'),
                                      ('Fermanagh', 'Fermanagh'), ('Waterford', 'Waterford'), ('Westmeath', 'Westmeath'),
                                      ('Wexford', 'Wexford'), ('Kerry', 'Kerry'), ('Kildare', 'Kildare'),
                                      ('Fermanagh', 'Fermanagh'), ('Wicklow', 'Wicklow')])

    submit = SubmitField('submit')


class CommentForm(FlaskForm):
    body = StringField('your comment', validators=[DataRequired(),Length(5,255)])
    rating = SelectField('rating', choices=[('5','5'), ('4.5', '4.5'), ('4', '4'), ('3.5', '3.5'),
                                      ('3', '3'), ('2.5', '2.5'), ('2', '2'), ('1.5', '1.5'), ('1', '1')])
    submit = SubmitField('Submit')

