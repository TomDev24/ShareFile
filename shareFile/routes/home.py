from flask import url_for, redirect, render_template, send_from_directory, session
from flask import Blueprint
from shareFile.components.FileEntry.model import FileEntry, SharedFiles
from shareFile.components.User.model import User
from shareFile.components.User.auth import cur_user

home_route = Blueprint("home_route", __name__)

@home_route.route("/")
@home_route.route("/home")
def home():
    permited_files = []
    current_user = cur_user(session.get("id"))
    if current_user:
        permited_files = User.query.get(current_user.id).shared_files
        permited_files_id = [f.file for f in permited_files]
        permited_files = FileEntry.query.filter(FileEntry.id.in_(permited_files_id)).all()
    public_files = FileEntry.get_public_files()
    all_files = sorted(public_files + permited_files, key=lambda d: d.download_amount, reverse=True)
    return render_template("home.html", files=all_files, current_user=current_user)

@home_route.route("/files/<file_path>")
def get_file(file_path):
    file_entry = FileEntry.by_file_path(file_path)
    current_user = cur_user(session.get("id"))
    if not file_entry:
        return redirect(url_for("home_route.home"))
    if file_entry.access == 0 and not current_user:
        return redirect(url_for("home_route.home"))
    if file_entry.access == 0 and current_user and file_entry.user_id != current_user.id:
        return redirect(url_for("home_route.home"))
    if file_entry.access == 1 and current_user:
        SharedFiles.permit_access(file_entry, current_user)
    FileEntry.update_download_amount(file_entry)
    return send_from_directory("static", "FileCollection/" + file_path)
