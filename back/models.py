from back import db


class Users(db.Model):
    uid_users = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), nullable=False)
    username = db.Column(db.String(255), nullable=False)
    hash_pass = db.Column(db.String(255), nullable=False)
    img = db.Column(db.String(255), nullable=True)
    first_name = db.Column(db.String(255), nullable=True)
    second_name = db.Column(db.String(255), nullable=True)


class News(db.Model):
    uid_news = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    text = db.Column(db.String(500), nullable=False)
    img = db.Column(db.String(255), nullable=True)
    fk_users = db.Column(db.Integer, db.ForeignKey('users.uid_users'), nullable = False)