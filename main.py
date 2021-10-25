from flask import Flask, url_for, render_template, request, session, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import asc, desc
from config import Config
from random import randint
import json

import smtplib
import hashlib
import os

app = Flask(__name__)
app.config.from_object(Config)  # applying all config to app
db = SQLAlchemy(app)

WTF_CSRF_ENABLED = True
WTF_CSRF_SECRET_KEY = 'sup3r_secr3t_passw3rd'

EMAIL_ADDRESS = "limct1232@gmail.com" # for sending email account
EMAIL_PASSWORD = "vcquwfgmlnoobuvi"

import models
from forms import Login_Form, Forgot_Form, Sign_Form, Change_Form, Comment_Form

@app.route('/')
def home():
    if session.get('name') != None: # checking if user is logged in or not
        pass
    else:
        session['name'] = "Guest"
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

            name_check = models.User.query.filter_by(name=name).first() # seeing if name is in databse

            if name_check is not None:
                salt = name_check.salt
                key = name_check.key
                new_key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000) # hashing password to check
                if key == new_key:
                    session['name'] = name
                    return redirect(url_for("login_post"))
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

        name_check = models.User.query.filter_by(name=name).first() #seeing if name or email is in databse
        email_check = models.User.query.filter_by(email=email).first()

        if name_check is None:
            if email_check is None:
                salt = os.urandom(32)
                key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000) # hashing salting

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
        if form.validate_on_submit():
            form = Forgot_Form()
            email = form.email.data

            global email_check # check if email is in database
            email_check = models.User.query.filter_by(email=email).first()

            if email_check == None:
                return redirect(url_for("login_post"))
            else:
                if email_check is not None:

                    global password_change # storing the change password
                    password_change = randint(10000, 99999)

                    with smtplib.SMTP('smtp.gmail.com', 587) as smtp: #how i send email
                        smtp.ehlo()
                        smtp.starttls()
                        smtp.ehlo()
                        smtp.login(EMAIL_ADDRESS,EMAIL_PASSWORD) # email and password for the email i set up also at top of code

                        subject = "your a loser"
                        body = f"your new password is {password_change}" # password code

                        msg = f'subject:{subject}\n\n{body}' # the message in the email

                        smtp.sendmail("limct1232@gmail.com", email, msg)

                    return redirect(url_for("password"))

                else:
                    form = Forgot_Form()
                    return render_template('forgot.html', page_title="forgot", user = current_user, form=form)




@app.route('/password', methods=['POST', 'GET'])
def password():

    current_user = session.get('name')
    form = Change_Form()
    if request.method == 'POST' and "code" in request.form:
        code = request.form['code'] # code that they enetered

        if password_change == int(code):
            current_user = models.User.query.filter_by(email=email_check.email).first()
            user = current_user.name
            print(user)
            form = Change_Form()
            return render_template('user.html', page_title="user", user = user, form= form)
        else:
            status = "wrong code" # if they eneter code wrong
            return render_template('password.html', page_title="password", user = current_user, status = status)
    return render_template('password.html', page_title="password", user = current_user)



@app.route('/map', methods=['POST', 'GET'])
def map():

    if request.method=='GET':
        current_user = session.get('name')
        period = 1
        clans  = models.Faction.query.all()

        locations  = models.Location.query.all()
        location = [] # getting the locations and putting them in a list with names
        for i in range(len(locations)):
            location.append(locations[i].name)


        factions = models.Location_Faction.query.filter_by(period = period).all()
        faction= [] # getting the locations and putting them in a list with faction number
        for i in range(len(factions)):
            faction.append(factions[i].fid)

        return render_template('map.html', page_title="map", user = current_user, location = location, faction = faction,clan=clans)
    else:
        a = like()
        print(a)
        return render_template('map.html', page_title="map", user = current_user, location = location, faction = faction,clan=clans)


@app.route('/maps', methods = ['POST'])
def like():
    period = json.loads(request.get_data()) # getting the data from map page
    period = period.get('likes')
    locations  = models.Location.query.all()
    location = []
    for i in range(len(locations)):
        location.append(locations[i].name)

    clans  = models.Faction.query.all()

    factions = models.Location_Faction.query.filter_by(period = period).all()
    faction= []
    for i in range(len(factions)):
        faction.append(factions[i].fid)

    return(str(loacation))


@app.route('/question', methods=['POST', 'GET'])
def question():
    current_user = session.get('name')
    form = Comment_Form()
    if request.method=='GET':
        questions = models.Question.query.all()

        return render_template('question.html', form=form, title="Question", user = current_user, questions = questions)
    else:

        questions = models.Question.query.all()

        if request.method == 'POST' and "recent" in request.form:

            questions = models.Question.query.order_by(models.Question.id.desc()).all() # seeing recent post using ids decesnding
            return render_template('question.html', form=form, page_title="history", user = current_user, questions = questions)

        if request.method == 'POST' and "last" in request.form:
            questions = models.Question.query.all() # seeing late post using ids
            return render_template('question.html', form=form, page_title="history", user = current_user, questions = questions)

        return render_template('question.html', form=form, page_title="history", user = current_user, questions = questions)


@app.route('/question/create', methods=['POST', 'GET'])
def create():
    if session.get('name') == "Guest":
        return redirect(url_for("login_post")) # if the user is ot logged in

    current_user = session.get('name')
    form = Comment_Form()
    user = session.get('name')

    questions = models.Question.query.all()

    if request.method == 'POST' and "title" in request.form:

        user = models.User.query.filter_by(name = session['name']).first()
        print(user)
        userid = user.id #

        title = request.form['title']
        content = request.form['content']

        user = models.Question(question=content, title=title, user = user.id)
        db.session.add(user)
        db.session.commit()

        questions = models.Question.query.all()

        return redirect(url_for("question"))

    return render_template('create.html', page_title="create", user = current_user, questions = questions,form=form)


@app.route('/comment/<id>', methods=['POST', 'GET']) # getting what comment goes where
def create_comment(id):
    form = Comment_Form()
    current_user = session.get('name')
    user = session['name']
    user = models.Comment(comment=form.comment.data, qid=id, user=user)
    db.session.add(user)
    db.session.commit()

    questions = models.Question.query.all()
    return render_template('question.html', page_title="create",  questions = questions, form=form)




@app.route('/user', methods=['POST', 'GET'] )
def user():

    if session.get('name') == None:
        return redirect(url_for("login_post"))
    current_user = session.get('name')

    form = Change_Form()
    user = models.User.query.filter_by(name = session['name']).first()

    if request.method=='GET':
        return render_template('user.html', form=form, title="User", user = current_user, stats = user)

    else:
        if request.method == 'POST' and "logout" in request.form:
            session['name'] = None
            return redirect(url_for("home"))

        elif form.validate_on_submit(): # changing their password
            password = form.password.data

            user = models.User.query.filter_by(name = session['name']).first()

            salt = os.urandom(32)
            key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)

            user.salt = salt
            user.key = key

            db.session.merge(user) # changing their password
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
