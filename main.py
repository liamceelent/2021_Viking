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


@app.route('/login', methods=['POST'])
def login():
    
    return render_template('login.html', page_title="Login")



if __name__ == "__main__":
    app.run(debug=True)
