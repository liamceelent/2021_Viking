from main import db


class User(db.Model):
    __tablename__ = "User"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(225), unique=True)
    salt = db.Column(db.String(225))
    key = db.Column(db.String(225))
    email = db.Column(db.String())


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


class Comment(db.Model):
    __tablename__ = "Comment"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    comment = db.Column(db.String(225), unique=True)
    qid = db.Column(db.Integer, db.ForeignKey('Question.id'), nullable = False)

    question = db.relationship('Question', back_populates = 'comments')

    def __repr__(self):
        return self.comment


class Question(db.Model):
    __tablename__ = "Question"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user = db.Column(db.Integer, db.ForeignKey('User.id'), nullable = False)
    question = db.Column(db.String(225), unique=True)
    title = db.Column(db.String(225), unique=True)

    comments = db.relationship('Comment', back_populates='question')
    users = db.relationship('User')


Visited = db.Table('Visited', db.Model.metadata,
    db.Column('Famous_id', db.Integer, db.ForeignKey('Famous_Viking.id')),
    db.Column('Location_id', db.Integer, db.ForeignKey('Location.id'))
)






db.create_all()
