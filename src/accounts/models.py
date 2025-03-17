from sqlalchemy import inspect
from datetime import datetime
from flask_validator import ValidateEmail, ValidateString, ValidateCountry
from sqlalchemy.orm import validates
from argon2 import PasswordHasher  # Import Argon2 PasswordHasher
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

    # Initialize the Argon2 Password Hasher
    ph = PasswordHasher()

    @classmethod
    def __declare_last__(cls):
        ValidateEmail(Account.email, True, True, "Invalid email address")
        ValidateString(Account.username, True, True, "Username must be a valid string")

    def set_password(self, password):
        """Hash the password using Argon2 and store the hashed password"""
        self.hashed_password = self.ph.hash(password)

    def check_password(self, password):
        """Check the provided password against the stored hashed password"""
        try:
            return self.ph.verify(self.hashed_password, password)
        except:
            return False  # If the password doesn't match, return False

    def toDict(self):
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}

    def __repr__(self):
        return f"<Account {self.username}>"