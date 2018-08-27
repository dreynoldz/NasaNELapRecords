# project/server/admin/forms.py


from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Email, Length, EqualTo

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

class UpdateUserForm(FlaskForm):
    admin = BooleanField('Admin')

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