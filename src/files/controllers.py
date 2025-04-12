import os
from src.accounts.models import Account # type: ignore
from flask import render_template, session

# ----------------------------------------------- #

def create_user_dirs():
    users = Account.query.all()
    for user in users:
        dir_path = os.path.join("files/users", user.username)
        os.makedirs(dir_path, exist_ok=True)

# ----------------------------------------------- #

def user_files_view():
    username = session.get('username')

    base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "users"))
    user_dir = os.path.join(base_path, username)

    os.makedirs(user_dir, exist_ok=True)

    try:
        files = os.listdir(user_dir)
    except Exception:
        files = []

    return render_template("files.html", files=files)