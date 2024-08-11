from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, TextAreaField, PasswordField
from wtforms.validators import DataRequired, Email, Length, EqualTo, Optional

class JobBoardScraperEmailForm(FlaskForm):
    email = StringField('email', validators=[DataRequired(), Email()])
    recaptcha = RecaptchaField()

class SendMeEmailForm(FlaskForm):
    user_email = StringField('email', validators=[DataRequired(), Email()])
    message = TextAreaField('message', render_kw={"rows": 10, "cols": 20}, validators=[DataRequired()])
    recaptcha = RecaptchaField()

class LoginForm(FlaskForm):
    username = StringField('username', validators=[DataRequired(), Length(min=4, max=20)])
    password = PasswordField('password', validators=[DataRequired()])

class SignUpForm(FlaskForm):
    username = StringField('username', validators=[DataRequired(), Length(min=4, max=30, message="Must be between 4 and 30 characters")])
    email = StringField('email', validators=[DataRequired(), Email()])
    full_name = StringField('full name', validators=[Optional()])
    password = PasswordField('password', validators=[DataRequired(),
                                                     Length(min=8, message='Password must be a minimum of 8 characters'),
                                                     EqualTo('confirm', message='Passwords must match')
                                                     ])
    confirm = PasswordField('confirm password')
                                                                      
