import os
from src.accounts.models import Account # type: ignore
from flask import render_template, session, request, send_from_directory, abort, redirect, url_for, flash
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

    return redirect(url_for('home'))

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
    return redirect(url_for('home'))

# ----------------------------------------------- #

def rename_files():
    username = session.get('username')
    if not username:
        return redirect(url_for('accounts.login'))

    base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "users"))
    user_dir = os.path.join(base_path, username)

    old_filename = request.form.get('old_filename')
    new_filename = request.form.get('new_filename')

    if not old_filename or not new_filename:
        flash("Both old and new filenames must be provided.")
        return redirect(url_for('home'))

    # Sanitize filenames
    old_filename = secure_filename(old_filename)
    new_filename = secure_filename(new_filename)

    # Extract the extension from the old filename
    _, file_extension = os.path.splitext(old_filename)

    # Append the original extension to the new filename if not present
    if not os.path.splitext(new_filename)[1]:
        new_filename += file_extension

    old_path = os.path.join(user_dir, old_filename)
    new_path = os.path.join(user_dir, new_filename)

    if not os.path.exists(old_path):
        flash(f"The file '{old_filename}' does not exist.")
        return redirect(url_for('home'))

    if os.path.exists(new_path):
        flash(f"A file named '{new_filename}' already exists.")
        return redirect(url_for('home'))

    try:
        os.rename(old_path, new_path)
        flash(f"File renamed from '{old_filename}' to '{new_filename}'.")
    except PermissionError:
        flash("Permission denied: unable to rename the file.")
    except Exception as e:
        flash(f"An error occurred: {str(e)}")

    return redirect(url_for('home'))

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
    return redirect(url_for('home'))

# ----------------------------------------------- #

def download_files():
    username = session.get('username')
    base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "users"))
    user_dir = os.path.join(base_path, username)

    filename = request.args.get('filename')  # con download meglio usare GET
    if not filename:
        return "Missing filename", 400

    file_path = os.path.join(user_dir, filename)

    if not os.path.isfile(file_path):
        return abort(404)

    return send_from_directory(user_dir, filename, as_attachment=True)









