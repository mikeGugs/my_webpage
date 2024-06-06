import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config():
    DEBUG = True
    SECRET_KEY = '2zTEjfiUXwY4rffFvJ7w0NiR3E6Plt'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'database.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    NEW_JOBS_PATH = '/Users/MikeGuglielmo/Desktop/python_code.py/job_board_scraper/new_jobs'
    MAIL_SENDER = 'webguglielmo@gmail.com'
    RECIPIENT_EMAIL = "webguglielmo@gmail.com"
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    RECAPTCHA_PUBLIC_KEY = os.environ.get('RECAPTCHA_PUBLIC_KEY')
    RECAPTCHA_PRIVATE_KEY = os.environ.get('RECAPTCHA_PRIVATE_KEY')
    
