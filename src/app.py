import os
from flask import session, render_template, redirect, url_for
from src.accounts.urls import accounts
from . import create_app

app = create_app(os.getenv("CONFIG_MODE", "default"))
app.secret_key = os.getenv("SECRET_KEY")

app.register_blueprint(accounts, url_prefix='/accounts', template_folder='views')

# ----------------------------------------------- #

@app.route('/')
def hello():
    return "Hello World!"

# ----------------------------------------------- #

@app.route('/home')
def home():
    if 'loggedin' in session:
        return render_template('home.html', username=session['username'])
    return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(debug=True)