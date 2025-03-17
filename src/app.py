import os
from flask import session, render_template, redirect, url_for
from flask_login import LoginManager
from src.accounts.models import Account # type: ignore
from src.accounts.urls import accounts # type: ignore
from . import create_app

app = create_app(os.getenv("CONFIG_MODE", "default"))
app.secret_key = os.getenv("SECRET_KEY")

#apps blueprint
app.register_blueprint(accounts, url_prefix='/accounts', template_folder='views')

# Initialize LoginManager for user authentication management
login_manager = LoginManager()
login_manager.login_view = "accounts.login"  # Set the login view endpoint
login_manager.init_app(app)  # Attach LoginManager to the Flask app


# Define user loader function to retrieve user object from the database
@login_manager.user_loader
def load_user(user_id):
    return Account.query.get(int(user_id))

# ----------------------------------------------- #

@app.route('/')
def root():
    return redirect(url_for('home'))

# ----------------------------------------------- #

@app.route('/home')
def home():
    if 'loggedin' in session:
        return render_template('home.html', username=session['username'])
    return redirect(url_for('accounts.login'))

# run app in debug mode if script is executed directly
if __name__ == "__main__":
    app.run(debug=True)