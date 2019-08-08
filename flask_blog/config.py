import os

class  Config:

    # set up a key for the application for security
    # import secrets
    # secrets.token_hex



    # SECRET_KEY = '3f75dbba084dfb3ef4dc7d14fbb661f0'

    SECRET_KEY = os.environ.get("SECRET_KEY")


    # configuring the database for flask_sqlalchemy

    # SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'

    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')


    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('EMAIL_USER')
    MAIL_PASSWORD = os.environ.get('EMAIL_PASS')
