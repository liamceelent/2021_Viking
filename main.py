from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from config import Config


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


@app.route('/sign_up')
def sign_up():

    return render_template('sign.html', page_title="Login")


@app.route('/forgot')
def forgot():

    return render_template('forgot.html', page_title="forgot")


@app.route('/login', methods=['POST'])
def login_post():

    return render_template('login.html', page_title="Login")


@app.route('/map')
def map():

    return render_template('map.html', page_title="map")


@app.route('/history')
def history():

    return render_template('history.html', page_title="history")


@app.route('/equipment', methods=['POST'])
def equipment():

    return render_template('equipment.html', page_title="equipment")


if __name__ == "__main__":
    app.run(debug=True)
