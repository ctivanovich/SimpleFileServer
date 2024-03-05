import os
import shutil

from io import BytesIO
from flask import Flask, request, redirect, url_for, make_response
from flask.typing import ResponseReturnValue
from flask_session import Session
from werkzeug.utils import secure_filename

from config.server_config import FLASK_MAX_FILE_SIZE

UPLOAD_FOLDER = "./uploads"
ALLOWED_EXTENSIONS = {"txt", "pdf", "png", "jpg", "jpeg", "gif"}

app = Flask(__name__)

app.secret_key = "super secret key"
app.config["SESSION_TYPE"] = "filesystem"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = FLASK_MAX_FILE_SIZE


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/", methods=["GET"])
def get_file_list() -> ResponseReturnValue:
    if os.listdir(UPLOAD_FOLDER) > 0:
        make_response("\n".join(os.listdir(UPLOAD_FOLDER)), 200)
    else:
        make_response("Currently there are no files.", 200)


@app.route("/upload=<filename>", methods=["POST"])
def upload_file(filename) -> ResponseReturnValue:
    # ensure folder exists
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

    # check if the post request has the file
    if "file" not in request.files:
        print(request.files)
        return make_response("No file provided", 400)
    
    file = request.files["file"]
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
        return make_response(f"{filename} uploaded successfully!", 200)
    else:
        return make_response(
            "Cannot upload file. Large files and files not of the allowed types cannot be handled.\
            Please consult the documentation for allowed types, and inspect size value in server settings.",
            400
        )

@app.route("/delete=<filename>", methods=["DELETE"])
def delete_file(filename) -> ResponseReturnValue:
    allowed = allowed_file(filename)
    path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    if allowed_file(filename) and os.path.isfile(path):
        os.remove(os.path.join(app.config["UPLOAD_FOLDER"], filename))
        return make_response(f"{filename} successfully deleted!", 200)
    else:
        return make_response("File not found, check path and name and try again. \
            Removing entire directories not supported.", 404)


def create_app():
    return app

if __name__ == "__main__":
    session = Session()
    session.init_app(app)
    app.run()