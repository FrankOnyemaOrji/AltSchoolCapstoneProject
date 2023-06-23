from config import db
from flask_login import UserMixin
from sqlalchemy.sql import func
import string
from random import choices


# UserMixin is a class that provides default implementations for the methods that Flask-Login expects user objects to
# have. It provides a generic User class that can be used to represent users in your application. If you are using a
# database along with Flask-Login, you will need to provide a user_loader callback.

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    username = db.Column(db.String(150), unique=True)
    links = db.relationship('Link', backref='user', lazy=True)


class Link(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original_url = db.Column(db.String(150))
    short_url = db.Column(db.String(150), unique=True)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.short_url = self.generate_short_link()

    def generate_short_link(self):
        characters = string.digits + string.ascii_letters
        short_url = ''.join(choices(characters, k=5))

        link = self.query.filter_by(short_url=short_url).first()

        if link:
            return self.generate_short_link()
        else:
            return short_url
