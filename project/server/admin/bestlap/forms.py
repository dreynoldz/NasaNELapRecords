# project/server/admin/bestlap/forms.py


from flask_wtf import FlaskForm
from wtforms import SelectField, DateField, FloatField, BooleanField
from wtforms.validators import DataRequired, Email, Length, EqualTo, NumberRange

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
