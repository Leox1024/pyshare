import os
from flask import Flask, session, render_template, redirect, url_for
from . import create_app  # Importa la funzione di inizializzazione
from .accounts.urls import accounts_bp  # Importa il Blueprint delle routes

# Crea l'app Flask
app = create_app(os.getenv("CONFIG_MODE", "default"))  # Usa "default" se CONFIG_MODE non è impostato
app.secret_key = os.getenv("SECRET_KEY")

# Registra il Blueprint delle routes
app.register_blueprint(accounts_bp, url_prefix='/accounts')

# ----------------------------------------------- #

# Hello World!
@app.route('/')
def hello():
    return "Hello World!"

# ----------------------------------------------- #

@app.route('/home')
def home():
    # Check if the user is logged in
    if 'loggedin' in session:
        # User is loggedin show them the home page
        return render_template('home.html', username=session['username'])
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))


if __name__ == "__main__":
    app.run(debug=True)  # Modalità debug per sviluppo