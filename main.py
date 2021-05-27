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
    return render_template('home.html', page_title="Home")


@app.route('/login')
def login():

    return render_template('login.html', page_title="Login")


@app.route('/login', methods=['POST'])
def login_post():
    if request.method == 'POST' and "name" in request.form:

        name = request.form['name']
        password = request.form['pass']

        name_check = models.User.query.filter_by(name=name).first()
        print(name_check)
        print("2")
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

    return render_template('login.html', page_title="Login")



@app.route('/sign_up')
def sign_up():

    return render_template('sign.html', page_title="Sign_up")


@app.route('/sign_up', methods=['POST'])
def sign_up_post():

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

    return render_template('sign.html', page_title="Sign_up",status= status)



@app.route('/forgot')
def forgot():

    return render_template('forgot.html', page_title="forgot")


@app.route('/map')
def map():

    return render_template('map.html', page_title="map")


@app.route('/history')
def history():

    return render_template('history.html', page_title="history")


@app.route('/equipment')
def equipment():

    return render_template('equipment.html', page_title="equipment")


if __name__ == "__main__":
    app.run(debug=True)
