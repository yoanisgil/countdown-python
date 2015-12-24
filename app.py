import os
from flask import Flask, request
from flask import render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from flask import Response
from forms import CountdownForm
from flask.ext.sqlalchemy import SQLAlchemy
import pytz
from datetime import datetime

def create_app():
    app = Flask(__name__)
    Bootstrap(app)

    return app

app = create_app()

@app.before_first_request
def create_tables():
    with app.app_context():
        db.create_all()

app_path = os.path.dirname(os.path.realpath(__file__))

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////%s' % (os.path.join(os.environ['DB_DIR'], 'app.db'))
app.config['CSRF_ENABLED'] = True
app.config['SECRET_KEY'] = '8}8:qvJs2UL2vs24+qUHPw)60ZZp@L'
app.config['DEBUG'] = os.environ['APP_DEBUG']
app.config['TIMEZONE'] = os.environ.get('TIMEZONE', 'America/New_York')

db = SQLAlchemy(app)

class Countdown(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text())
    year = db.Column(db.Integer)
    month = db.Column(db.Integer)
    day = db.Column(db.Integer)
    hour = db.Column(db.Integer)
    minute = db.Column(db.Integer)


    def __init__(self, name, year, month, day, hour, minute):
        self.name = name
        self.year = year
        self.month = month
        self.day = day
        self.hour = hour
        self.minute = minute

    def __repr__(self):
        return '<Countdown %r>' % self.name

    @property
    def seconds_to_end(self):
        tz = pytz.timezone(app.config['TIMEZONE'])
        loc_dt = tz.localize(datetime(self.year, self.month, self.day, self.hour, self.minute))
        utc_now = pytz.utc.localize(datetime.utcnow())
        loc_now = tz.normalize(utc_now.astimezone(tz))

        if loc_now < loc_dt:
            return int((loc_dt - loc_now).total_seconds())

        return 0


@app.route("/", methods=['GET', 'POST'])
def index():
    app.logger.debug('Index page')

    form = CountdownForm(request.form)

    if request.method == 'POST' and form.validate():
        count_down = Countdown(form.name.data, form.year.data, form.month.data, form.day.data, form.hour.data,
                               form.minute.data)
        db.session.add(count_down)
        db.session.commit()

        app.logger.debug('Created new countdown with id %s' % count_down.id)

        return redirect(url_for('countdown', countdown_id=count_down.id))

    tz = pytz.timezone(app.config['TIMEZONE'])
    utc_now = pytz.utc.localize(datetime.utcnow())
    now = tz.normalize(utc_now.astimezone(tz))

    form.year.data = now.year
    form.month.data = now.month
    form.day.data = now.day
    form.hour.data = now.hour
    form.minute.data = now.minute

    return render_template('index.html', form=form)


@app.route('/v/<int:countdown_id>')
def countdown(countdown_id):
    count_down = Countdown.query.filter_by(id=countdown_id).first()
    
    if not count_down:
        app.logger.error('404 on countdown with id %s' % countdown_id)
        return render_template('404.html', countdown_id=countdown_id), 404

    return render_template('countdown.html', countdown=count_down)


if __name__ == "__main__":
    host = os.environ.get('APP_LISTEN_ON', '0.0.0.0')
    app.run(host=host)
