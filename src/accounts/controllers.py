from flask import request, redirect, url_for, flash, session
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import login_user
from src import db
from src.accounts.models import Account
import re

def login_controller():
    username = request.form['username']
    password = request.form['password']

    account = Account.query.filter_by(username=username).first()

    if account and check_password_hash(account.hashed_password, password):
        session['loggedin'] = True
        session['id'] = account.id
        session['username'] = account.username

        login_user(account)
        flash("Logged in successfully!", "success")
        return redirect(url_for('home'))
    else:
        
        flash("Incorrect username/password!", "danger")
        return redirect(url_for('accounts.login'))
    
def register_controller():
    username = request.form['username']
    password = request.form['password']
    email = request.form['email']

    account = Account.query.filter_by(username=username).first()

    if account:
        flash("Account already exists!", "danger")
    elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
        flash("Invalid email address!", "danger")
    elif not re.match(r'[A-Za-z0-9]+', username):
        flash("Username must contain only letters and numbers!", "danger")
    else:
        hashed_password = generate_password_hash(password)

        new_account = Account(username=username, email=email)
        new_account.set_password(password)
        db.session.add(new_account)
        db.session.commit()
        db.session.add(new_account)
        db.session.commit()

        flash("You have successfully registered!", "success")
        return redirect(url_for('accounts.login'))