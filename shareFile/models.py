from shareFile import db, login_manager
from datetime import datetime
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    files = db.relationship('FileEntry', backref='author', lazy=True)
    shared_files = db.relationship('SharedFiles', backref='shared_with', lazy=True)

    def __repr__(self):
        return f'User {self.username}, {self.email}, {self.id}'

class SharedFiles(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    file = db.Column(db.Integer, db.ForeignKey('file_entry.id'), nullable=False)

class FileEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    filename = db.Column(db.String(80), nullable=False)
    access = db.Column(db.Integer, nullable=False) # 0 - for one; 1- for one with link; 2 - for everybody
    download_amount = db.Column(db.Integer, nullable=False)
    file_path = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f'User {self.date_posted}, {self.id}'