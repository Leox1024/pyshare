from sqlalchemy import inspect
from datetime import datetime
from flask_validator import ValidateEmail, ValidateString, ValidateCountry
from sqlalchemy.orm import validates
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from src import db  # Importa l'oggetto `db` da __init__.py

# ----------------------------------------------- #

class Account(db.Model, UserMixin):  # UserMixin permette di usare Flask-Login
    __tablename__ = 'accounts'  # Nome della tabella in PostgreSQL

    # Campi della tabella
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    hashed_password = db.Column(db.String(255), nullable=False)  # 🔹 Salvare password hashata
    created_at = db.Column(db.DateTime(timezone=True), default=datetime.utcnow)
    updated_at = db.Column(db.DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)

    # Validazioni con Flask-Validator
    @classmethod
    def __declare_last__(cls):
        ValidateEmail(Account.email, True, True, "Invalid email address")
        ValidateString(Account.username, True, True, "Username must be a valid string")

    # Hash della password prima di salvarla nel DB
    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    # Verifica della password
    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)

    # Metodo per serializzare i dati in JSON (utile per API REST)
    def toDict(self):
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}

    def __repr__(self):
        return f"<Account {self.username}>"