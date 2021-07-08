from flask import Flask, url_for, render_template, request, session, redirect
from flask_sqlalchemy import SQLAlchemy
from config import Config

import hashlib
import os

app = Flask(__name__)
app.config.from_object(Config)  # applying all config to app
db = SQLAlchemy(app)


import models


@app.route('/')
def home():
    if session.get('name') != None:
        pass
    else:
        session['name'] = None
    current_user = session.get('name')
    return render_template('home.html', page_title="Home", user = current_user)



@app.route('/login', methods=['POST', 'GET'])
def login_post():
    if request.method == 'POST' and "name" in request.form:

        name = request.form['name']
        password = request.form['pass']

        name_check = models.User.query.filter_by(name=name).first()

        if name_check is not None:
            salt = name_check.salt
            key = name_check.key
            new_key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
            if key == new_key:
                session['name'] = name
                return redirect(url_for("home"))
            else:
                status = "Wrong user name or password."
                return render_template('login.html', status=status)
        else:
            status = "Wrong user name or password."
            return render_template('login.html', status=status)
    else:
        return render_template('login.html', page_title="Login")



@app.route('/sign_up', methods=['POST', 'GET'])
def sign_up_post():
    if request.method == 'POST' and "sign_name" in request.form:
        name = request.form['sign_name']
        password = request.form['sign_pass']

        name_check = models.User.query.filter_by(name=name).first()

        if name_check is None:
            salt = os.urandom(32)
            key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)

            user = models.User(name=name, salt=salt, key=key)
            db.session.add(user)
            db.session.commit()
            session['name'] = name
            return redirect(url_for("home"))
        else:
            status = "Name Already Taken"
            return render_template('sign.html', page_title="Sign_up",status= status)
    else:
        return render_template('sign.html', page_title="Sign_up")



@app.route('/forgot')
def forgot():
    current_user = session.get('name')
    return render_template('forgot.html', page_title="forgot", user = current_user)


@app.route('/map')
def map():
    current_user = session.get('name')
    return render_template('map.html', page_title="map", user = current_user)


@app.route('/history')
def history():
    current_user = session.get('name')
    return render_template('history.html', page_title="history", user = current_user)

@app.route('/user', methods=['POST', 'GET'] )
def user():

    if session.get('name') == None:
        return redirect(url_for("login_post"))
    current_user = session.get('name')

    image = models.Image.query.all()
    if request.method == 'POST' and "logout" in request.form:
        session['name'] = None
        return redirect(url_for("home"))

    user = models.User.query.filter_by(name = session['name']).first()

    image = user.image
    print(image)

    return render_template('user.html', page_title="user", user = current_user, images = image)



@app.route('/famous', methods=['POST', 'GET'])
def famous():
    famous_vikings = models.Famous_Viking.query.all()
    current_user = session.get('name')
    return render_template('famous.html', page_title="famous", vikings = famous_vikings, user = current_user)

@app.route('/famous_click', methods=['POST', 'GET'])
def famous_click():
    current_user = session.get('name')

    viking_id = request.args.get('viking_id')
    print(viking_id)
    stats = models.Famous_Viking.query.filter_by(id = viking_id).all()
    print(stats)
    return render_template('famous_click.html', page_title="famous", user = current_user, stats = stats)

if __name__ == "__main__":
    app.run(debug=True)
