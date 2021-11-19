from shareFile import db
from datetime import datetime
from shareFile.utils.utils import save_file

class SharedFiles(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    file = db.Column(db.Integer, db.ForeignKey('file_entry.id'), nullable=False)

    @classmethod
    def permit_access(cls, file_entry, current_user):
        new_shared = SharedFiles(file=file_entry.id, user_id=current_user.id)
        db.session.add(new_shared)
        db.session.commit()

class FileEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    filename = db.Column(db.String(80), nullable=False)
    access = db.Column(db.Integer, nullable=False) # 0 - for one; 1- for one with link; 2 - for everybody
    download_amount = db.Column(db.Integer, nullable=False)
    file_path = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    shared_with = db.relationship('SharedFiles', backref='file_shared', lazy=True)

    @classmethod
    def get_public_files(cls):
        return FileEntry.query.filter_by(access=2).order_by(FileEntry.download_amount.desc()).all()

    @classmethod
    def update_download_amount(cls, file_entry):
        file_entry.download_amount += 1
        db.session.commit()

    @classmethod
    def by_file_path(cls, file_path):
        return FileEntry.query.filter_by(file_path=file_path).first()

    @classmethod
    def upload_file(cls, form, current_user):
        _, new_filename = save_file(form.file.data)
        new_file = FileEntry(file_path=new_filename, access=form.access_setting.data, download_amount=0,
                            filename=form.filename.data, user_id=current_user.id)
        db.session.add(new_file)
        db.session.commit()

    @classmethod
    def get_user_files(cls, current_user):
        return FileEntry.query.filter_by(user_id=current_user.id).all()

    def __repr__(self):
        return f'User {self.date_posted}, {self.id}'
