from flask import Flask

from flask_sqlalchemy import SQLAlchemy
# import os
from os import path
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "scissor.db"
DB_NAMEB = "postgres://scissor_url_user:6SY4OzRAyxYlk6ero2xeVUckBYybMC4p@dpg-ciejshtgkuvlk1gf70a0-a.oregon-postgres.render.com/scissor_url"


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'fd8fefa4bea22a413d1bd730ef391b0d'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://scissor_url_user:6SY4OzRAyxYlk6ero2xeVUckBYybMC4p@dpg-ciejshtgkuvlk1gf70a0-a.oregon-postgres.render.com/scissor_url'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    #f'sqlite:///{DB_NAME}'
    # postgres://scissor_url_user:6SY4OzRAyxYlk6ero2xeVUckBYybMC4p@dpg-ciejshtgkuvlk1gf70a0-a.oregon-postgres.render.com/scissor_url
    db.init_app(app)

    from shorts import short
    from auth import auth
    app.register_blueprint(short, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from models import User

    with app.app_context():
        db.create_all()

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'  # if the user is not logged in, redirect them to the login page
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app


# @app.before_first_request
def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')
