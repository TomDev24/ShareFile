from flask import url_for, current_app
import os
import secrets

def save_file(form_file):
    random_hex = secrets.token_hex(8)
    f_name, f_ext = os.path.splitext(form_file.filename)
    new_filename = random_hex + f_ext
    new_file_path = os.path.join(current_app.root_path, 'static/', 'FileCollection/', new_filename)
    form_file.save(new_file_path)
    relative_path = url_for('static', filename='FileCollection/' + new_filename)
    return relative_path, new_filename
