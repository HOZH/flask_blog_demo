from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flask_blog.config import Config
# from datetime import datetime


db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
# tell the exetion which function is working with login feature
login_manager.login_view = 'users.login'
# bridging a content for using as a css class name later
login_manager.login_message_category = 'info'


# print(app.config['MAIL_USE_TLE'])
# print(app.config['MAIL'])


mail = Mail()


#from flask_blog import db
# db.create_all()


def create_app(config_class=Config):

    app = Flask(__name__)

    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    from flask_blog.users.routes import users
    from flask_blog.posts.routes import posts
    from flask_blog.main.routes import main
    from flask_blog.errors.handlers import errors

    app.register_blueprint(users)
    app.register_blueprint(main)
    app.register_blueprint(posts)
    app.register_blueprint(errors)


    return app
