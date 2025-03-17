from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, logout_user, current_user
from .controllers import login_controller, register_controller
from src.accounts.models import Account # type: ignore

accounts = Blueprint("accounts", __name__, template_folder='views')

# ----------------------------------------------- #

@accounts.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return login_controller()

    return render_template('index.html')

# ----------------------------------------------- #

@accounts.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for('accounts.login'))

# ----------------------------------------------- #

@accounts.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        return register_controller()
    return render_template('register.html')

# ----------------------------------------------- #

@accounts.route('/profile')
@login_required
def profile():
    account = Account.query.get(current_user.id)
    
    if account:
        return render_template('profile.html', account=account)
    
    return redirect(url_for('accounts.login'))