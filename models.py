from main import db


class User(db.Model):
    __tablename__ = "User"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(225), unique=True)
    salt = db.Column(db.String(225))
    key = db.Column(db.String(225))

class Location(db.Model):
    __tablename__ = "Location"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(225), unique=True)

class Faction(db.Model):
    __tablename__ = "Faction"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(225), unique=True)

class Location_Faction(db.Model):
    __tablename__ = "Location_Faction"
    id = db.Column(db.Integer, primary_key=True)
    lid = db.Column(db.Integer, db.ForeignKey('Location.id'), nullable = False)
    fid = db.Column(db.Integer, db.ForeignKey('Faction.id'), nullable = False)
    period = db.Column(db.Integer)

class Famous_Viking(db.Model):
    __tablename__ = "Famous_Viking"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(225), unique=True)
    age = db.Column(db.Integer)
    fid = db.Column(db.Integer, db.ForeignKey('Faction.id'), nullable = False)
    wid = db.Column(db.Integer, db.ForeignKey('Weapon.id'), nullable = False)
    kill = db.Column(db.Integer)

class Weapon(db.Model):
    __tablename__ = "Weapon"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(225), unique=True)

Visted = db.Table('Visted', db.Model.metadata,
    db.Column('Famous_id', db.Integer, db.ForeignKey('Famous_Viking.id')),
    db.Column('Location_id', db.Integer, db.ForeignKey('Location.id'))
)





db.create_all()
