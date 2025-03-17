from sqlalchemy import inspect
from datetime import datetime
from flask_validator import ValidateEmail, ValidateString, ValidateCountry
from sqlalchemy.orm import validates
from argon2 import PasswordHasher
from flask_login import UserMixin
from .. import db

# ----------------------------------------------- #

class Account(db.Model, UserMixin):
    __tablename__ = 'accounts'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    hashed_password = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), default=datetime.utcnow)
    updated_at = db.Column(db.DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)

    ph = PasswordHasher()

    @classmethod
    def __declare_last__(cls):
        ValidateEmail(Account.email, True, True, "Invalid email address")
        ValidateString(Account.username, True, True, "Username must be a valid string")

    def set_password(self, password):
        self.hashed_password = self.ph.hash(password)

    def check_password(self, password):
        try:
            return self.ph.verify(self.hashed_password, password)
        except:
            return False

    def toDict(self):
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}

    def __repr__(self):
        return f"<Account {self.username}>"