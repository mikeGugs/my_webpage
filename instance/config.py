import os

basedir = os.path.abspath(os.path.dirname(__file__))
print(basedir)

DEBUG = True
SECRET_KEY = 'hard to guess string'
#SECRET_KEY = '2zTEjfiUXwY4rffFvJ7w0NiR3E6Plt'
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'database.db')
print(SQLALCHEMY_DATABASE_URI)
SQLALCHEMY_TRACK_MODIFICATIONS = False
