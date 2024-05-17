import os
from flask import Flask, render_template, url_for, request, redirect, session, flash, current_app
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired, Email
from flask_mail import Mail, Message
from threading import Thread


app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile('config.py')

db = SQLAlchemy(app)

mail = Mail(app)

class JobBoardScraperEmails(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(80), unique=True, nullable=False)

    def __repr__(self):
        return f'<User {self.email}>'


class JobBoardScraperEmailForm(FlaskForm):
    email = StringField('email', validators=[DataRequired(), Email()])

class SendMeEmailForm(FlaskForm):
    user_email = StringField('email', validators=[DataRequired(), Email()])
    message = TextAreaField('message', render_kw={"rows": 10, "cols": 20}, validators=[DataRequired()])
                        
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
def job_board_scraper():
    with open(app.config['NEW_JOBS_PATH']) as jobs:
        j = jobs.read()
        
    form = JobBoardScraperEmailForm()
    error = None
    if request.method == 'POST':
        if form.validate_on_submit():
            email = JobBoardScraperEmails.query.filter_by(email=form.email.data).first()
            if email is None:
                email = JobBoardScraperEmails(email=form.email.data)
                db.session.add(email)
                db.session.commit()
                flash("Thank you for subscribing!")
            else:
                error = f"{form.email.data} is already subscribed!"
        else:
            error = f"{form.email.data} is an invalid email address. Please enter a valid email address"
            
    return render_template('job_board_scraper.html', jobs=j, form=form, error=error)

@app.route('/unsubscribe', methods=('GET', 'POST'))
def unsubscribe():
    form = JobBoardScraperEmailForm()
    error = None
    if request.method == 'POST':
        if form.validate_on_submit():
            email = JobBoardScraperEmails.query.filter_by(email=form.email.data).first()
            if email is None:
                error = f"{form.email.data} is not currently subscribed!"
            else:
                db.session.delete(email)
                db.session.commit()
                flash(f"{email} has been unsubscribed.")
        else:
            error = f"{form.email.data} is an invalid email address. Please enter a valid email address"
            
    return render_template('unsubscribe.html', form=form, error=error)

@app.route('/about_me')
def about_me():
    return render_template('about_me.html')

@app.route('/contact', methods=('GET', 'POST'))
def contact():
    form = SendMeEmailForm()
    error = None
    if request.method == 'POST':
      if form.validate_on_submit():
          user_email = form.user_email.data
          message = form.message.data
          send_me_email(user_email, message)
          flash("Thanks for sending me a message!")
      else:
          error = f"{form.user_email.data} is not a valid email address. Please enter a valid email address."
    return render_template('contact.html', form=form, error=error)


def send_async_email(msg, app):
    with app.app_context():
        mail.send(msg)

def send_me_email(from_email, message):
    app = current_app._get_current_object()
    msg_subject = f"You have a new email from {from_email}"
    msg = Message(sender=app.config['MAIL_SENDER'],
                  recipients=[app.config['RECIPIENT_EMAIL']],
                  body=message,
                  subject=msg_subject
                  )
    thr = Thread(target=send_async_email, args=[msg, app])
    thr.start()
    return thr
