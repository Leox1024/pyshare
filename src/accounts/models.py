from sqlalchemy import inspect
from datetime import datetime
from sqlalchemy.orm import validates
from argon2 import PasswordHasher
from flask_login import UserMixin
from marshmallow import Schema, fields, validate, ValidationError
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

    @validates("email")
    def validate_email(self, key, email):
        """ Valida l'email al momento dell'inserimento nel DB """
        schema = AccountSchema()
        errors = schema.validate({"email": email})
        if errors:
            raise ValidationError(errors["email"])
        return email

    @validates("username")
    def validate_username(self, key, username):
        """ Valida l'username al momento dell'inserimento nel DB """
        schema = AccountSchema()
        errors = schema.validate({"username": username})
        if errors:
            raise ValidationError(errors["username"])
        return username

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

# ----------------------------------------------- #

class AccountSchema(Schema):
    """ Schema per validare i dati con Marshmallow """
    email = fields.Email(required=True, error_messages={"invalid": "Invalid email address"})
    username = fields.Str(
        required=True, 
        validate=validate.Length(min=3, max=100), 
        error_messages={"invalid": "Username must be a valid string"}
    )
