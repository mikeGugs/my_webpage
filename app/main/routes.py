from app.main import bp
from flask import Flask, render_template, url_for, request, redirect, session, flash, current_app
from app.extensions import db
from app.models import JobBoardScraperEmails
from app.forms.forms import JobBoardScraperEmailForm, SendMeEmailForm
from app.utils import send_async_email, send_me_email


@bp.route('/')
def index():
    return render_template('home.html')

@bp.route('/bond_portfolio_analyzer')
def bond_portfolio_analyzer():
    return render_template('bond_portfolio_analyzer.html')

@bp.route('/job_board_scraper', methods=('GET', 'POST'))
def job_board_scraper():
    with open(current_app.config['NEW_JOBS_PATH']) as jobs:
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
                message = f"New subscriber: {email}"
                msg_subject = f"New Job Board Scraper Email Subscriber!"
                send_me_email(email, msg_subject, message)
                flash("Thank you for subscribing!")
            else:
                error = f"{form.email.data} is already subscribed!"
        else:
            error = f"{form.email.data} is an invalid email address. Please enter a valid email address"
            
    return render_template('job_board_scraper.html', jobs=j, form=form, error=error)

@bp.route('/unsubscribe', methods=('GET', 'POST'))
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

@bp.route('/about_me')
def about_me():
    return render_template('about_me.html')

@bp.route('/contact', methods=('GET', 'POST'))
def contact():
    form = SendMeEmailForm()
    error = None
    if request.method == 'POST':
      if form.validate_on_submit():
          user_email = form.user_email.data
          message = form.message.data
          msg_subject = f"You have a new email from {user_email}"
          send_me_email(user_email, msg_subject, message)
          flash("Thanks for sending me a message!")
      else:
          error = f"{form.user_email.data} is not a valid email address. Please enter a valid email address."
    return render_template('contact.html', form=form, error=error)
