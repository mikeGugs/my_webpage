from app.auth import auth_bp
from flask import Flask, render_template, url_for, request, redirect, session, flash, current_app
from app.extensions import db
from app.forms.forms import LoginForm, SignUpForm

@auth_bp.route('/login', methods=('GET', 'POST'))
def login():
    form = LoginForm()
    error = None
    if request.method == 'POST':
      if form.validate_on_submit():
          username = form.username.data
          password = form.password.data
      else:
          error = f"Please check your credentials, and try again."
    return render_template('login.html', form=form, error=error)


@auth_bp.route('/signup')
def signup():
    # NEED TO MAKE THIS PAGE SHOW CORRECT ERRORS
    form = SignUpForm()
    error = None
    if request.method == 'POST':
      if form.validate_on_submit():
          username = form.username.data
          email = form.email.data
          password = form.password.data
      else:
          error = f"Please check your credentials, and try again."
    return render_template('signup.html', form=form, error=error)

@auth_bp.route('/logout')
def logout():
    return 'Logout'
