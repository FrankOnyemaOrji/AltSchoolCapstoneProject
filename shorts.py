from flask import Blueprint, render_template, request, redirect
from flask_login import current_user
from models import User, Link
from config import db

short = Blueprint('short', __name__)


@short.route('/<short_url>')
def redirect_to_url(short_url):
    link = Link.query.filter_by(short_url=short_url).first_or_404()
    db.session.add(link)
    db.session.commit()
    link.date_created = link.date_created.strftime('%d/%m/%Y')
    return redirect(link.original_url, link.date_created)


@short.route('/')
def index():
    links = Link.query.all()
    return render_template('index.html', user=current_user, links=links)


@short.route('/add_link', methods=['POST'])
def add_link():
    original_url = request.form.get('original_url')
    link = Link(original_url=original_url)
    links = Link.query.all()
    db.session.add(link)
    db.session.commit()
    return render_template('display.html', short_url=link.short_url, original_url=link.original_url, user=current_user, date_created=link.date_created, links=links)

# @short.errorhandler(404)
# def page_not_found(e):
#     return render_template('404.html'), 404
