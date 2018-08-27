# project/server/admin/forms.py


from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, Email, Length, EqualTo

class TrackForm(FlaskForm):
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