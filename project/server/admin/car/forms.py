# project/server/admin/car/forms.py


from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, Length, EqualTo

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