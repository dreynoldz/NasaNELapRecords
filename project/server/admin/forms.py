# project/server/admin/forms.py


from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SelectMultipleField, DateField, \
    FloatField, SelectField
from wtforms.validators import DataRequired, Email, Length, EqualTo, NumberRange

class CreateUserForm(FlaskForm):
    email = StringField(
        'Email Address',
        validators=[
            DataRequired(),
            Email(message=None),
            Length(min=6, max=40)
        ]
    )
    password = PasswordField(
        'Password',
        validators=[DataRequired(), Length(min=6, max=25)]
    )
    confirm = PasswordField(
        'Confirm password',
        validators=[
            DataRequired(),
            EqualTo('password', message='Passwords must match.')
        ]
    )
    admin = BooleanField('Admin')
    racer = SelectField('Racer', choices=[], coerce=int)

class UpdateUserForm(FlaskForm):
    admin = BooleanField('Admin')
    racer = SelectField('Racer', choices=[], coerce=int)

class passwordResetForm(FlaskForm):
    email = StringField(
        'Email Address',
        validators=[
            DataRequired(),
            Email(message=None),
            Length(min=6, max=40)
        ]
    )
    password = PasswordField(
        'Password',
        validators=[DataRequired(), Length(min=6, max=25)]
    )
    confirm = PasswordField(
        'Confirm password',
        validators=[
            DataRequired(),
            EqualTo('password', message='Passwords must match.')
        ]
    )

class NameSNForm(FlaskForm):
    name = StringField(
        'Name',
        validators=[
            DataRequired(),
            Length(min=6, max=80)
        ]
    )
    short_name = StringField(
        'Short Name',
        validators=[DataRequired()]
    )

class EventForm(FlaskForm):
    name = StringField(
        'Name',
        validators=[
            DataRequired(),
            Length(min=5, max=40)
        ]
    )
    start_date = DateField(
        'Start Date',
        validators=[DataRequired()]
    )
    end_date = DateField(
        'End Date',
        validators=[DataRequired()]
    )
    tracks = SelectMultipleField('Track', choices=[], coerce=int)

class SponsorForm(FlaskForm):
    name = StringField(
        'Name',
        validators=[
            DataRequired(),
            Length(min=6, max=80)
        ]
    )

class CarForm(FlaskForm):
    make = StringField(
        'Make',
        validators=[
            DataRequired(),
            Length(min=6, max=80)
        ]
    )
    model = StringField(
        'Model',
        validators=[
            DataRequired(),
            Length(min=1, max=80)
        ]
    )
    year = StringField(
        'Year',
        validators=[
            DataRequired(),
            Length(min=4, max=4)
        ]
    )
    color = StringField(
        'Color',
        validators=[
            DataRequired(),
            Length(min=2, max=80)
        ]
    )
    number = StringField(
        'Number',
        validators=[
            DataRequired(),
            Length(min=1, max=10)
        ]
    )

class BestLapForm(FlaskForm):
    racer = SelectField('Racer', choices=[], coerce=int)
    raceclass = SelectField('Race Class', choices=[], coerce=int)
    event = SelectField('Event', choices=[], coerce=int)
    time = FloatField('Time',
        validators=[
            DataRequired()
        ]
    )
    lap_date = DateField(
        'Lap Date',
        validators=[DataRequired()]
    )
    is_best = BooleanField('Best Lap?')