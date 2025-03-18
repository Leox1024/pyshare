from flask import request, redirect, url_for, flash, session
from flask_login import login_user
from argon2 import PasswordHasher
from email_validator import validate_email, EmailNotValidError
from src import db  # type: ignore
from src.accounts.models import Account  # type: ignore
import re

ph = PasswordHasher()

# ----------------------------------------------- #

def is_valid_email(email):
    try:
        validate_email(email)
        return True
    except EmailNotValidError:
        return False

def is_valid_username(username):
    return re.match(r"^[A-Za-z0-9]{3,100}$", username)

# ----------------------------------------------- #

def login_controller():
    user_input = request.form['username']
    password = request.form['password']

    account = Account.query.filter_by(username=user_input).first() or Account.query.filter_by(email=user_input).first()

    if account:
        try:
            if ph.verify(account.hashed_password, password):
                session['loggedin'] = True
                session['id'] = account.id
                session['username'] = account.username

                login_user(account)
                flash("Logged in successfully!", "success")
                return redirect(url_for('home'))
        except:
            flash("Incorrect username/email or password!", "danger")

    else:
        flash("Incorrect username/email or password!", "danger")

    return redirect(url_for('accounts.login'))

# ----------------------------------------------- #

def register_controller():
    username = request.form['username']
    password = request.form['password']
    email = request.form['email']

    if Account.query.filter_by(username=username).first():
        flash("Account already exists!", "danger")

    elif not is_valid_email(email):
        flash("Invalid email address!", "danger")

    elif not is_valid_username(username):
        flash("Username must contain only letters and numbers!", "danger")

    else:
        hashed_password = ph.hash(password)

        new_account = Account(username=username, email=email, hashed_password=hashed_password)
        db.session.add(new_account)
        db.session.commit()

        flash("You have successfully registered!", "success")
        return redirect(url_for('accounts.login'))

    return redirect(url_for('accounts.register'))