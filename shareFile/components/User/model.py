from shareFile import db, bcrypt

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    files = db.relationship('FileEntry', backref='author', lazy=True)
    shared_files = db.relationship('SharedFiles', backref='shared_with', lazy=True)

    def __repr__(self):
        return f'User {self.username}, {self.email}, {self.id}'

    @classmethod
    def create_user(cls, form):
        hash_password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        new_user = User(username=form.username.data, email=form.email.data, password=hash_password)
        db.session.add(new_user)
        db.session.commit()

    @classmethod
    def by_user_email(cls, email):
        return User.query.filter_by(email=email).first()
