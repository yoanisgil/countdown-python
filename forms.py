__author__ = 'Yoanis Gil'

from flask_wtf import Form
from wtforms import IntegerField, StringField
from wtforms import validators


class CountdownForm(Form):
    name = StringField('name', validators=[validators.Length(min=5)], default='')
    year = IntegerField('year', validators=[validators.NumberRange(min=2015)])
    month = IntegerField('month', validators=[validators.NumberRange(min=01, max=12)])
    day = IntegerField('day', validators=[validators.NumberRange(min=01, max=31)])
    hour = IntegerField('hour', validators=[validators.NumberRange(min=0, max=23)])
    minute = IntegerField('minute', validators=[validators.NumberRange(min=0, max=59)])
