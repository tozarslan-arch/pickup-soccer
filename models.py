from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Location(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False, unique=True)
    address = db.Column(db.String(255), nullable=False)

    def map_url(self):
        from urllib.parse import quote_plus
        return f"https://www.google.com/maps/search/?api=1&query={quote_plus(self.address)}"


class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    location_id = db.Column(db.Integer, db.ForeignKey('location.id'), nullable=False)
    date_time = db.Column(db.DateTime, nullable=False)
    target = db.Column(db.Integer, nullable=True)
    note = db.Column(db.String(255), nullable=True)

    location = db.relationship('Location', backref='events')
    votes = db.relationship('Vote', backref='event', cascade="all, delete-orphan")

    @property
    def vote_count(self):
        return len(self.votes)

    @property
    def is_on(self):
        return self.target is not None and self.vote_count >= self.target


class Vote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
