import os
from dotenv import load_dotenv

from flask import Flask, session, render_template, redirect, url_for, flash
from flask_login import LoginManager, login_required
from flask_wtf.csrf import CSRFProtect
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from . import create_app
from src.accounts.models import Account # type: ignore
from src.accounts.urls import accounts # type: ignore
from src.accounts.controllers import limiter # type: ignore

from src.files.controllers import create_user_dirs # type: ignore
from src.files.urls import files # type: ignore
# ----------------------------------------------- #

# Load .env value from parent directory
dotenv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
load_dotenv(dotenv_path)

app = create_app(os.getenv("CONFIG_MODE", "default"))
app.secret_key = os.getenv("SECRET_KEY", "default_secret_key")


# ----------------------------------------------- #

#app init
with app.app_context():
    create_user_dirs()
limiter.init_app(app)
csrf = CSRFProtect(app)

#blueprint config
app.register_blueprint(accounts, url_prefix='/accounts', template_folder='views')
app.register_blueprint(files, url_prefix='/files', template_folder='views')

#cookie session config
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_PERMANENT'] = False

# ----------------------------------------------- #

login_manager = LoginManager()
login_manager.login_view = "accounts.login"
login_manager.init_app(app)

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
    username = session.get('username')
    if not username:
        flash("Session expired or user not logged in")
        return redirect(url_for('accounts.login'))
    user_dir = os.path.join("files/users", username)

    try:
        files = os.listdir(user_dir)
    except FileNotFoundError:
        files = []

    return render_template('home.html', username=username, files=files)

# ----------------------------------------------- #