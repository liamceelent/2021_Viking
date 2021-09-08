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

WTF_CSRF_ENABLED = True
WTF_CSRF_SECRET_KEY = 'sup3r_secr3t_passw3rd'

EMAIL_ADDRESS = "limct1232@gmail.com"
EMAIL_PASSWORD = "vcquwfgmlnoobuvi"

import models
from forms import Login_Form, Forgot_Form, Sign_Form, Change_Form, Comment_Form

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

    form = Login_Form()
    current_user = session.get('name')
    if request.method=='GET':  # did the browser ask to see the page
        return render_template('login.html', form=form, title="Login", user = current_user)

    else:
        if form.validate_on_submit():
            name = form.name.data
            password = form.password.data

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
                    return render_template('login.html', status=status, form=form)
            else:
                status = "Wrong user name or password."
                return render_template('login.html', status=status, form=form)



@app.route('/sign_up', methods=['POST', 'GET'])
def sign_up_post():

    form = Sign_Form()
    current_user = session.get('name')

    if request.method=='GET':  # did the browser ask to see the page
        return render_template('sign.html', form=form, title="Login", user = current_user)
    else:

        name = form.name.data
        password = form.password.data
        email = form.email.data

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
                return render_template('sign.html', page_title="Sign_up",status= status, form=form)
        else:
            status = "Name is Already Taken"
            return render_template('sign.html', page_title="Sign_up",status= status, form=form)



@app.route('/forgot', methods=['POST', 'GET'])
def forgot():
    form = Forgot_Form()
    current_user = session.get('name')

    if request.method=='GET':  # did the browser ask to see the page
        return render_template('forgot.html', form=form, title="Forgot", user = current_user)
    else:

        email = request.form['email']

        global email_check
        email_check = models.User.query.filter_by(email=email).first()

        if email_check == None:
            return render_template('login.html')
        else:
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
            current_user = models.User.query.filter_by(email=email_check.email).first()
            user = current_user.name
            print(user)
            form = Change_Form()
            return render_template('user.html', page_title="user", user = user, form= form)
        else:
            status = "wrong code"
            return render_template('password.html', page_title="password", user = current_user, status = status)
    return render_template('password.html', page_title="password", user = current_user)



@app.route('/map', methods=['POST', 'GET'])
def map():

    if request.method=='GET':
        current_user = session.get('name')
        period = 1

        locations  = models.Location.query.all()
        location = []
        for i in range(len(locations)):
            location.append(locations[i].name)


        factions = models.Location_Faction.query.filter_by(period = period).all()
        faction= []
        for i in range(len(factions)):
            faction.append(factions[i].fid)

        return render_template('map.html', page_title="map", user = current_user, location = location, faction = faction)
    else:
        period = request.form.get("period")
        current_user = session.get('name')

        locations  = models.Location.query.all()
        location = []
        for i in range(len(locations)):
            location.append(locations[i].name)


        factions = models.Location_Faction.query.filter_by(period = period).all()
        faction= []
        for i in range(len(factions)):
            faction.append(factions[i].fid)

        return render_template('map.html', page_title="map", user = current_user, location = location, faction = faction)


@app.route('/question', methods=['POST', 'GET'])
def history():


    current_user = session.get('name')
    form = Comment_Form()

    if request.method=='GET':  # did the browser ask to see the page
        questions = models.Question.query.all()
        return render_template('question.html', form=form, title="Question", user = current_user, questions = questions)
    else:

        questions = models.Question.query.all()

        comment = form.comment.data



        return render_template('question.html', page_title="history", user = current_user, questions = questions)


@app.route('/question/create', methods=['POST', 'GET'])
def create():
    if session.get('name') == None:
        return redirect(url_for("login_post"))

    current_user = session.get('name')

    user = session.get('name')

    questions = models.Question.query.all()

    if request.method == 'POST' and "title" in request.form:

        user = models.User.query.filter_by(name = session['name']).first()
        userid = user.id

        title = request.form['title']
        content = request.form['content']

        user = models.Question(question=content, title=title, user = user.id)
        db.session.add(user)
        db.session.commit()

        questions = models.Question.query.all()
        return render_template('question.html', page_title="question", user = current_user, questions = questions)

    return render_template('create.html', page_title="create", user = current_user, questions = questions)

@app.route('/question/{{ question.id }}', methods=['POST', 'GET'])
def create_comment():

    return render_template('create.html', page_title="create", user = current_user, questions = questions)




@app.route('/user', methods=['POST', 'GET'] )
def user():

    if session.get('name') == None:
        return redirect(url_for("login_post"))
    current_user = session.get('name')

    form = Change_Form()
    user = models.User.query.filter_by(name = session['name']).first()

    if request.method=='GET':  # did the browser ask to see the page
        return render_template('user.html', form=form, title="User", user = current_user, stats = user)

    else:
        if request.method == 'POST' and "logout" in request.form:
            session['name'] = None
            return redirect(url_for("home"))

        elif form.validate_on_submit():
            password = form.password.data

            user = models.User.query.filter_by(name = session['name']).first()

            salt = os.urandom(32)
            key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)

            user.salt = salt
            user.key = key

            db.session.merge(user)
            db.session.commit()

            chan = "ture"
            return render_template('user.html', page_title="user", user = current_user, form = form, status = chan)

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
