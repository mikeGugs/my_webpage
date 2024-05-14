import os
from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func

app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile('config.py')

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(80), unique=True, nullable=False)

    def __repr__(self):
        return f'<User {self.email}>'

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/job_board_scraper', methods=('GET', 'POST'))
def projects():
    with open(app.config['NEW_JOBS_PATH']) as jobs:
        j = jobs.read()
    return render_template('job_board_scraper.html', jobs=j)

@app.route('/about_me')
def about_me():
    return render_template('about_me.html')

@app.route('/contact', methods=('GET', 'POST'))
def contact():
    return render_template('contact.html')
