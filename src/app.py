import os
from flask import Flask, session, render_template, redirect, url_for
from flask_login import LoginManager, login_required
from flask_wtf.csrf import CSRFProtect
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from src.accounts.models import Account  # type: ignore
from src.accounts.urls import accounts  # type: ignore
from . import create_app

# ----------------------------------------------- #

app = create_app(os.getenv("CONFIG_MODE", "default"))
app.secret_key = os.getenv("SECRET_KEY", "default_secret_key")  #fallback sk
limiter = Limiter(get_remote_address, app=app, default_limits=["5 per minute"])

csrf = CSRFProtect(app)

# ----------------------------------------------- #

app.register_blueprint(accounts, url_prefix='/accounts', template_folder='views')

# ----------------------------------------------- #

# init login manager
login_manager = LoginManager()
login_manager.login_view = "accounts.login"
login_manager.init_app(app)

# load user from active session
@login_manager.user_loader
def load_user(user_id):
    return Account.query.get(int(user_id)) if user_id.isdigit() else None

# ----------------------------------------------- #

@login_required
@app.route('/')
def root():
    return redirect(url_for('home'))

# ----------------------------------------------- #

@login_required
@app.route('/home')
def home():
    return render_template('home.html', username=session['username']) if 'loggedin' in session else redirect(url_for('accounts.login'))