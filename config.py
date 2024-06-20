import os
from dotenv import load_dotenv

load_dotenv()

class ProductionConfig():
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_LOCATION')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    NEW_JOBS_PATH = os.environ.get('NEW_JOBS_PATH')
    MAIL_SENDER = 'webguglielmo@gmail.com'
    RECIPIENT_EMAIL = "webguglielmo@gmail.com"
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    RECAPTCHA_PUBLIC_KEY = os.environ.get('RECAPTCHA_PUBLIC_KEY')
    RECAPTCHA_PRIVATE_KEY = os.environ.get('RECAPTCHA_PRIVATE_KEY')
    

class TestingConfig():
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('TESTING_DATABASE_LOCATION')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    NEW_JOBS_PATH = os.environ.get('NEW_JOBS_PATH')
    MAIL_SENDER = 'webguglielmo@gmail.com'
    RECIPIENT_EMAIL = "webguglielmo@gmail.com"
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    RECAPTCHA_PUBLIC_KEY = os.environ.get('RECAPTCHA_PUBLIC_KEY')
    RECAPTCHA_PRIVATE_KEY = os.environ.get('RECAPTCHA_PRIVATE_KEY')
    
