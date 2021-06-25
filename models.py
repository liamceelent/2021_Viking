from main import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(225), unique=True)
    salt = db.Column(db.String(225))
    key = db.Column(db.String(225))

class Location(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(225), unique=True)

class Faction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(225), unique=True)

class Location_Faction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    lid = db.Column(db.Integer, db.ForeignKey('location.id'), nullable = False)
    fid = db.Column(db.Integer, db.ForeignKey('faction.id'), nullable = False)
    period = db.Column(db.Integer)

db.create_all()
