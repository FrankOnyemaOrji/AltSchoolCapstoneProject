from flask import Blueprint, render_template, request, flash, redirect, url_for
from models import User
from werkzeug.security import generate_password_hash, check_password_hash
from config import db
from flask_login import login_user, login_required, logout_user, current_user


auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email') # get the email from the form
        password = request.form.get('password') # get the password from the form

        user = User.query.filter_by(email=email).first() # check if the user exists in the database
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('short.index'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')
    return render_template("login.html", user=current_user) # render the login page


@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('username') # get the username from the form
        password1 = request.form.get('password1') # get the password from the form
        password2 = request.form.get('password2') # get the password from the form

        user_exists = User.query.filter_by(email=email).first() # check if the user exists in the database
        username_exists = User.query.filter_by(username=username).first() # check if the username exists in the database

        if user_exists:
            flash('Email already exists.', category='error')
        elif username_exists:
            flash('Username already exists.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(username) < 4:
            flash('Username is too short.', category='error')
        elif len(password1) < 7:
            flash('Password is too short.', category='error')
        elif len(email) < 4:
            flash('Email is invalid.', category='error')
        else:
            new_user = User(email=email, username=username, password=generate_password_hash(password1, method='sha256'))
            db.session.add(new_user) # add the new user to the database
            db.session.commit() # commit the changes
            login_user(new_user, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('short.index')) # redirect the user to the home page
    return render_template("register.html", user=current_user) # render the register page


@auth.route('/logout')
@login_required # this decorator ensures that the user is logged in before they can access this route
def logout():
    logout_user()
    return redirect(url_for('auth.login'))