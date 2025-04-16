from flask import Blueprint
from .controllers import user_files_view, files_upload

files = Blueprint("files", __name__, template_folder='views')

@files.route("/", methods=['GET'])
def user_files():
    return user_files_view()

@files.route("/upload", methods=["POST"])
def files_upload_route():
    return files_upload()