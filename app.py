from flask import Flask, request
from flask import render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from forms import CountdownForm
from flask.ext.sqlalchemy import SQLAlchemy
from pytz import timezone
from datetime import datetime


def create_app():
    app = Flask(__name__)
    Bootstrap(app)

    return app

app = create_app()

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
app.config['CSRF_ENABLED'] = True
app.config['SECRET_KEY'] = '8}8:qvJs2UL2vs24+qUHPw)60ZZp@L'

db = SQLAlchemy(app)


class Countdown(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text())
    year = db.Column(db.Integer)
    month = db.Column(db.Integer)
    day = db.Column(db.Integer)
    hour = db.Column(db.Integer)
    minute = db.Column(db.Integer)
    timezone = db.Column(db.String(80))

    def __init__(self, name, year, month, day, hour, minute, timezone):
        self.name = name
        self.year = year
        self.month = month
        self.day = day
        self.hour = hour
        self.minute = minute
        self.timezone = timezone

    def __repr__(self):
        return '<Countdown %r>' % self.name

    @property
    def seconds_to_end(self):
        tz = timezone(self.timezone)
        loc_dt = tz.localize(datetime(self.year, self.month, self.day, self.hour, self.minute))
        loc_now = tz.localize(datetime.now())

        if loc_now < loc_dt:
            return int((loc_dt - loc_now).total_seconds())

        return 0


@app.route("/", methods=['GET', 'POST'])
def index():
    form = CountdownForm(request.form)

    if request.method == 'POST' and form.validate():
        count_down = Countdown(form.name.data, form.year.data, form.month.data, form.day.data, form.hour.data,
                               form.minute.data,
                               'America/Chicago')
        db.session.add(count_down)
        db.session.commit()

        return redirect(url_for('countdown', countdown_id=count_down.id))

    return render_template('index.html', form=form)


@app.route('/v/<int:countdown_id>')
def countdown(countdown_id):
    count_down = Countdown.query.filter_by(id=countdown_id).first()

    return render_template('countdown.html', countdown=count_down)


if __name__ == "__main__":
    app.run(debug=True)
