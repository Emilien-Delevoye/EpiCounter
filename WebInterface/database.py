
# Table db

import datetime as d_time
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Count(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    update = db.Column(db.Integer, nullable=False)
    room = db.Column(db.String(200), nullable=False)
    door = db.Column(db.String(200), nullable=False)
    total = db.Column(db.Integer, nullable=False)
    total_raw = db.Column(db.Integer, nullable=True)
    date_created = db.Column(db.TIMESTAMP, default=d_time.datetime.utcnow, nullable=False)

    def __repr__(self):
        return '<id: %r>' % id

