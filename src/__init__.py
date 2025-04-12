from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

from jinja2 import ChoiceLoader, FileSystemLoader

from .config import config

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()

def create_app(config_mode):
    app = Flask(__name__)
    app.jinja_loader = ChoiceLoader([
        FileSystemLoader("src/accounts/views"),
        FileSystemLoader("src/files/views")
    ])
    app.config.from_object(config[config_mode])

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    return app


@login_manager.user_loader
def load_user(user_id):
    from accounts.models import Account
    return Account.query.get(int(user_id))