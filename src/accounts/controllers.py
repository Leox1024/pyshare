import re

from flask import request, redirect, url_for, flash, session
from flask_login import login_user

from argon2 import PasswordHasher
from email_validator import validate_email, EmailNotValidError
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from src import db # type: ignore
from src.accounts.models import Account # type: ignore
from src.files.controllers import create_user_dirs # type: ignore

# ----------------------------------------------- #

limiter = Limiter(key_func=get_remote_address)

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

@limiter.limit("5 per minute")
def login_controller():
    user_input, password = request.form.get('username'), request.form.get('password')

    if not user_input or not password:
        flash("Username/email and password are required!", "danger")
        return redirect(url_for('accounts.login'))

    account = Account.query.filter((Account.username == user_input) | (Account.email == user_input)).first()

    if account and PasswordHasher().verify(account.hashed_password, password):
        session.update({'loggedin': True, 'id': account.id, 'username': account.username})
        login_user(account)
        flash("Logged in successfully!", "success")
        return redirect(url_for('home'))

    flash("Incorrect username/email or password!", "danger")
    return redirect(url_for('accounts.login'))

# ----------------------------------------------- #

@limiter.limit("3 per minute")
def register_controller():
    username, password, email = request.form.get('username'), request.form.get('password'), request.form.get('email')

    if Account.query.filter_by(username=username).first():
        flash("Account already exists!", "danger")
    elif not is_valid_email(email):
        flash("Invalid email address!", "danger")
    elif not is_valid_username(username):
        flash("Username must contain only letters and numbers!", "danger")
    else:
        db.session.add(Account(username=username, email=email, hashed_password=PasswordHasher().hash(password)))
        db.session.commit()
        flash("You have successfully registered!", "success")
        create_user_dirs()
        return redirect(url_for('accounts.login'))

    return redirect(url_for('accounts.register'))