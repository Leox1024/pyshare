from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager  # 🔹 Aggiunto Flask-Login

from .config import config

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()  # 🔹 Aggiunto LoginManager

def create_app(config_mode):
    app = Flask(__name__)
    app.config.from_object(config[config_mode])

    # Inizializza le estensioni
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)  # 🔹 Inizializza Flask-Login

    return app

# 🔹 Funzione per caricare l'utente dal database
@login_manager.user_loader
def load_user(user_id):
    from src.accounts.models import Account  # Import ritardato per evitare problemi di import circolare
    return Account.query.get(int(user_id))