from flask import Blueprint
from .controllers import user_files_view 

files = Blueprint("files", __name__, template_folder='views')

@files.route("/", methods=['GET'])
def user_files():
    return user_files_view()