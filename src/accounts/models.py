from sqlalchemy import inspect
from datetime import datetime
from flask_validator import ValidateEmail, ValidateString, ValidateCountry
from sqlalchemy.orm import validates
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from src import db

# ----------------------------------------------- #

class Account(db.Model, UserMixin):
    __tablename__ = 'accounts'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    hashed_password = db.Column(db.String(255), nullable=False)  # 🔹 Salvare password hashata
    created_at = db.Column(db.DateTime(timezone=True), default=datetime.utcnow)
    updated_at = db.Column(db.DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)

    @classmethod
    def __declare_last__(cls):
        ValidateEmail(Account.email, True, True, "Invalid email address")
        ValidateString(Account.username, True, True, "Username must be a valid string")

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)

    def toDict(self):
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}

    def __repr__(self):
        return f"<Account {self.username}>"