from db import db

class Note(db.Model):
    __tablename__ = "notes"
    id = db.Column(db.Integer(), primary_key=True)
    content = db.Column(db.Text)
    timings = db.relationship('Timing', backref=db.backref('notes'))

class Timing(db.Model):
    __tablename__ = "timings"
    id = db.Column(db.Integer(), primary_key=True)
    timestamp = db.Column(db.Integer)
    notes_id = db.Column(db.Integer, db.ForeignKey('notes.id'))