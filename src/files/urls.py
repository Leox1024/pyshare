from flask import Blueprint
from .controllers import user_files_view, files_upload, rename_files, delete_files, download_files

files = Blueprint("files", __name__, template_folder='views')

@files.route("/", methods=['GET'])
def user_files():
    return user_files_view()

@files.route("/upload", methods=['POST'])
def files_upload_route():
    return files_upload()

@files.route("/rename", methods=['POST'])
def rename_files_route():
    return rename_files()

@files.route("/delete", methods=['POST'])
def delete_files_route():
    return delete_files()

@files.route("/downlaod", methods=['GET'])
def download_files_route():
    return download_files()
