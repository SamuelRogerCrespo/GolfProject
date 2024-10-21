from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db  # Importing the database from __init__.py
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template("login.html", user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('first_name')  # Corrected field name
        last_name = request.form.get('last_name')  # Corrected field name
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        # Check for existing user with the same email
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.', category='error')
        elif email is None or len(email) < 4:  # Check for None and length
            flash('Email must be greater than 3 characters.', category='error')
        elif first_name is None or len(first_name) < 2:  # Check for None and length
            flash('First name must be greater than 1 character.', category='error')
        elif last_name is None or len(last_name) < 2:  # Validate last name length
            flash('Last name must be greater than 1 character.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            # Create a new user and store in the database
            new_user = User(email=email, first_name=first_name, last_name=last_name,
                            password=generate_password_hash(password1, method='pbkdf2:sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)  # Log the user in after creation
            flash('Account created!', category='success')
            return redirect(url_for('views.home'))

    return render_template("sign_up.html", user=current_user)
