from main import db


class User(db.Model):
    __tablename__ = "User"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(225), unique=True)
    salt = db.Column(db.String(225))
    key = db.Column(db.String(225))
    coin = db.Column(db.Integer, default = 0)
    img = db.Column(db.Integer, db.ForeignKey('Image.id'), default = 1)
    email = db.Column(db.String())

    image = db.relationship('Image', back_populates="user")

class Image(db.Model):
    __tablename__ = "Image"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(), unique=True)

    user = db.relationship('User', back_populates="image")




class Location(db.Model):
    __tablename__ = "Location"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(225), unique=True)

    faction = db.relationship('Location_Faction', back_populates='locations')

class Faction(db.Model):
    __tablename__ = "Faction"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(225), unique=True)

    location = db.relationship('Location_Faction', back_populates='factions')

class Location_Faction(db.Model):
    __tablename__ = "Location_Faction"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    lid = db.Column(db.Integer, db.ForeignKey('Location.id'), nullable = False)
    fid = db.Column(db.Integer, db.ForeignKey('Faction.id'), nullable = False)
    period = db.Column(db.Integer)

    locations = db.relationship('Location', back_populates="faction")
    factions = db.relationship('Faction', back_populates="location")

class Famous_Viking(db.Model):
    __tablename__ = "Famous_Viking"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(225), unique=True)
    age = db.Column(db.Integer)
    fid = db.Column(db.Integer, db.ForeignKey('Faction.id'), nullable = False)
    wid = db.Column(db.Integer, db.ForeignKey('Weapon.id'), nullable = False)
    kill = db.Column(db.Integer)
    rating = db.Column(db.Integer)
    description = db.Column(db.String())
    img = db.Column(db.String())

class Weapon(db.Model):
    __tablename__ = "Weapon"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(225), unique=True)




Visited = db.Table('Visited', db.Model.metadata,
    db.Column('Famous_id', db.Integer, db.ForeignKey('Famous_Viking.id')),
    db.Column('Location_id', db.Integer, db.ForeignKey('Location.id'))
)






db.create_all()
