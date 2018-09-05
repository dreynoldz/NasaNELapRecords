# project/server/admin/raacer/forms.py


from flask_wtf import FlaskForm
from wtforms import StringField, SelectMultipleField, DateField, IntegerField
from wtforms.validators import DataRequired, Email, Length, EqualTo, NumberRange

class RacerForm(FlaskForm):
    email = StringField(
        'Email Address',
        validators=[
            DataRequired(),
            Email(message=None),
            Length(min=6, max=40)
        ]
    )
    name = StringField(
        'Name',
        validators=[
            DataRequired(),
            Length(min=6, max=40)
        ]
    )
    city = StringField(
        'City',
        validators=[
            DataRequired(),
            Length(min=3, max=40)
        ]
    )
    state = StringField(
        'State',
        validators=[
            DataRequired(),
            Length(min=2, max=40)
        ]
    )
    points = IntegerField(
        'Points',
        validators=[
            DataRequired(),
            NumberRange(min=0, max=300)
        ]
    )
    cars = SelectMultipleField('Car', choices=[], coerce=int)
    sponsors = SelectMultipleField('Sponsor', choices=[], coerce=int)