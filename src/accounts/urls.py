import re
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from src import db
from src.accounts.models import Account
from .controllers import login_controller  # Import corretto

# Definizione del Blueprint per gli account
accounts_bp = Blueprint('accounts', __name__)

@accounts_bp.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return login_controller()  # Richiama il controller corretto

    return render_template('index.html')

@accounts_bp.route('/logout')
@login_required  # Assicura che l'utente sia loggato prima di eseguire il logout
def logout():
    # Logout dell'utente con Flask-Login
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for('accounts.login'))  # Corretto: usa il nome del Blueprint

@accounts_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']

        # Verifica se l'account esiste già
        account = Account.query.filter_by(username=username).first()

        if account:
            flash("Account already exists!", "danger")
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            flash("Invalid email address!", "danger")
        elif not re.match(r'[A-Za-z0-9]+', username):
            flash("Username must contain only letters and numbers!", "danger")
        else:
            # Hash della password in modo sicuro
            hashed_password = generate_password_hash(password)

            # Crea un nuovo utente
            new_account = Account(username=username, email=email)
            new_account.set_password(password)  # 🔹 Hash della password
            db.session.add(new_account)
            db.session.commit()
            db.session.add(new_account)
            db.session.commit()

            flash("You have successfully registered!", "success")
            return redirect(url_for('accounts.login'))

    return render_template('register.html')


@accounts_bp.route('/profile')
@login_required  # 🔹 Protegge la route: solo utenti loggati possono accedere
def profile():
    # Trova l'utente attuale nel database usando Flask-Login
    account = Account.query.get(current_user.id)

    if account:
        return render_template('profile.html', account=account)
    
    # Se l'utente non è trovato, reindirizza alla pagina di login
    return redirect(url_for('accounts.login'))