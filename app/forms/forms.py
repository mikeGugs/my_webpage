from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired, Email

class JobBoardScraperEmailForm(FlaskForm):
    email = StringField('email', validators=[DataRequired(), Email()])
    recaptcha = RecaptchaField()

class SendMeEmailForm(FlaskForm):
    user_email = StringField('email', validators=[DataRequired(), Email()])
    message = TextAreaField('message', render_kw={"rows": 10, "cols": 20}, validators=[DataRequired()])
    recaptcha = RecaptchaField()
