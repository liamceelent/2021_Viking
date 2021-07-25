from flask import Flask, url_for, render_template, request, session, redirect
from flask_sqlalchemy import SQLAlchemy
from config import Config
from random import randint

import smtplib
import hashlib
import os

app = Flask(__name__)
app.config.from_object(Config)  # applying all config to app
db = SQLAlchemy(app)

EMAIL_ADDRESS = "limct1232@gmail.com"
EMAIL_PASSWORD = "vcquwfgmlnoobuvi"

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
    current_user = session.get('name')

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
        return render_template('login.html', page_title="Login", user = current_user)



@app.route('/sign_up', methods=['POST', 'GET'])
def sign_up_post():
    current_user = session.get('name')

    if request.method == 'POST' and "sign_name" in request.form:
        name = request.form['sign_name']
        password = request.form['sign_pass']
        email = request.form['sign_email']

        name_check = models.User.query.filter_by(name=name).first()
        email_check = models.User.query.filter_by(email=email).first()

        if name_check is None:
            if email_check is None:
                salt = os.urandom(32)
                key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)

                user = models.User(name=name, salt=salt, key=key, email=email)
                db.session.add(user)
                db.session.commit()
                session['name'] = name
                return redirect(url_for("home"))
            else:
                status = "Email is Already Taken"
                return render_template('sign.html', page_title="Sign_up",status= status)
        else:
            status = "Name is Already Taken"
            return render_template('sign.html', page_title="Sign_up",status= status)
    else:
        return render_template('sign.html', page_title="Sign_up", user = current_user)



@app.route('/forgot', methods=['POST', 'GET'])
def forgot():
    current_user = session.get('name')

    if request.method == 'POST' and "email" in request.form:
        email = request.form['email']

        global email_check
        email_check = models.User.query.filter_by(email=email).first()

        if email_check is not None:

            global password_change
            password_change = randint(10000, 99999)

            with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
                smtp.ehlo()
                smtp.starttls()
                smtp.ehlo()
                smtp.login(EMAIL_ADDRESS,EMAIL_PASSWORD)

                subject = "your a loser"
                body = f"your new password is {password_change}"

                msg = f'subject:{subject}\n\n{body}'

                smtp.sendmail("limct1232@gmail.com", email, msg)

            return redirect(url_for("password"))

        else:
            return render_template('forgot.html', page_title="forgot", user = current_user)

    return render_template('forgot.html', page_title="forgot", user = current_user)

@app.route('/password', methods=['POST', 'GET'])
def password():

    current_user = session.get('name')

    if request.method == 'POST' and "code" in request.form:
        code = request.form['code']

        if password_change == int(code):
            current_user = models.User.query.filter_by(email=email_check).first()
            return render_template('user.html', page_title="user", user = current_user, status = statsus)
        else:
            status = "wrong code"
            return render_template('password.html', page_title="password", user = current_user, status = status)
    return render_template('password.html', page_title="password", user = current_user)



@app.route('/map')
def map():
    current_user = session.get('name')

    location = models.Location.query.all()

    viking_clans = models.Faction.query.all()
    print(viking_clans)
    return render_template('map.html', page_title="map", user = current_user, country = location, clan = viking_clans)


@app.route('/question')
def history():
    current_user = session.get('name')
    return render_template('question.html', page_title="history", user = current_user)

@app.route('/user', methods=['POST', 'GET'] )
def user():

    if session.get('name') == None:
        return redirect(url_for("login_post"))
    current_user = session.get('name')


    if request.method == 'POST' and "logout" in request.form:
        session['name'] = None
        return redirect(url_for("home"))

    user = models.User.query.filter_by(name = session['name']).first()


    image = user.image.name
    print(image)
    allimage =  models.Image.query.all()

    return render_template('user.html', page_title="user", user = current_user, image = image, stats = user, allimage = allimage)



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


@app.errorhandler(404)
def page_not_found(e):
    current_user = session.get('name')
    return render_template("404.html", user = current_user)

if __name__ == "__main__":
    app.run(debug=True)
