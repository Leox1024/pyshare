import os
from src.accounts.models import Account # type: ignore
from flask import render_template, session, request
from werkzeug.utils import secure_filename

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

# ----------------------------------------------- #

def files_upload():
    #get current session name
    username = session.get('username')
    base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "users"))
    user_dir = os.path.join(base_path, username)

    #upload file to user dir
    uploaded_file = request.files.get('file')
    if uploaded_file and uploaded_file.filename:
        filename = secure_filename(uploaded_file.filename)
        uploaded_file.save(os.path.join(user_dir, filename))

    # reload html
    files = os.listdir(user_dir)
    return render_template("home.html", files=files)

# ----------------------------------------------- #

def rename_files():
    #get current session name
    username = session.get('username')
    base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "users"))
    user_dir = os.path.join(base_path, username)

    old_filename = request.form.get('old_filename')
    new_filename = request.form.get('new_filename')

    # Rename the file
    old_path = os.path.join(user_dir, old_filename)
    new_path = os.path.join(user_dir, new_filename)

    try:
        os.rename(old_path, new_path)
    except FileNotFoundError:
        return "File not found", 404
    except Exception as e:
        return str(e), 500

    # reload html
    files = os.listdir(user_dir)
    return render_template("home.html", files=files)

# ----------------------------------------------- #

def delete_files():
    #get current session name
    username = session.get('username')
    base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "users"))
    user_dir = os.path.join(base_path, username)

    filename = request.form.get('filename')
    file_path = os.path.join(user_dir, filename)

    try:
        os.remove(file_path)
    except Exception as e:
        return str(e), 500

    # reload html
    files = os.listdir(user_dir)
    return render_template("home.html", files=files)












