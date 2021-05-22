from main import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(225), unique=True)
    salt = db.Column(db.String(225))
    key = db.Column(db.String(225))



class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    blog_post = db.Column(db.String(225))

db.create_all()
