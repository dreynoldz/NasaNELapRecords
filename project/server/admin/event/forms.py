# project/server/admin/forms.py


from flask_wtf import FlaskForm
from wtforms import StringField, SelectMultipleField, DateField
from wtforms.validators import DataRequired, Email, Length, EqualTo

class EventForm(FlaskForm):
    name = StringField(
        'Name',
        validators=[
            DataRequired(),
            Length(min=6, max=40)
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