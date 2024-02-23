import os
import shutil
from flask import Flask, request, redirect, url_for
from flask_session import Session
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = "./uploads"
ALLOWED_EXTENSIONS = {"txt", "pdf", "png", "jpg", "jpeg", "gif"}

app = Flask(__name__)

app.secret_key = "super secret key"
app.config["SESSION_TYPE"] = "filesystem"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = 16 * 1000 * 1000  ## 16 mb


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/", methods=["GET"])
def get_file_list() -> list:
    return "\n".join(os.listdir(UPLOAD_FOLDER))


@app.route("/upload=<filename>", methods=["POST"])
def upload_file(filename):
    # check if the post request has the file part
    if "file" not in request.files:
        return "No file provided"
    file = request.files["file"]

    if file.filename == "":
        return redirect(request.url)

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
        return "File uploaded successfully"
    return "File failed to upload. Is it larger than the maximum allowed 16 MB?"


@app.route("/delete=<filename>", methods=["DELETE"])
def delete_file(filename):
    allowed = allowed_file(filename)
    path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    if allowed_file(filename) and os.path.isfile(path):
        os.remove(os.path.join(app.config["UPLOAD_FOLDER"], filename))
        return "File deleted"
    else:
        return "File not found, check path and name and try again. Removing entire directories not supported."


app.add_url_rule("/", endpoint="get_file_list", build_only=True)
app.add_url_rule("/upload", endpoint="upload_file", build_only=True)
app.add_url_rule("/delete", endpoint="delete_file", build_only=True)

if __name__ == "__main__":
    session = Session()
    session.init_app(app)
    app.run()