from flask_wtf import FlaskForm
from wtforms import StringField, RadioField, BooleanField, SubmitField
from wtforms.validators import DataRequired


class ConfigForm(FlaskForm):
    language = RadioField('Language', choices=[('EN', 'English'), ('HU', 'Hungarian')], validators=[DataRequired()])
    max_word_length = RadioField('Max Word Length',
                                 choices=[(2, '2'), (3, '3'), (4, '4'), (5, '5'), (6, '6'), (7, '7'), (8, '8'),
                                          (9, '9'), (10, '10'), (11, '11'), (12, '12'), (13, '13')], coerce=int,
                                 validators=[DataRequired()])
    own_tileset = StringField('Enter your own tiles here (without any breaks):')
    only_max = BooleanField('Only Max Length?')
    submit = SubmitField('Send')
