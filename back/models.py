from back import db


class Users(db.Model):
    uid_user = db.Column(db.Integer, primary_key=True)
    fio = db.Column(db.String(500), nullable=False)
    hash_pass = db.Column(db.String(500), nullable=False)
    img = db.Column(db.String(500), nullable=True)
    telegram_name = db.Column(db.String(500), nullable=True)
    balance = db.Column(db.Integer, nullable=True)
    id_team = db.Column(db.Integer, db.ForeignKey('teams.id_team'), nullable=True)
    status = db.Column(db.Boolean, nullable=True)
    telegram_id = db.Column(db.String(500), nullable=False)


class Teams(db.Model):
    id_team = db.Column(db.Integer, primary_key=True)
    coord = db.Column(db.Integer, nullable=True)
    team_name = db.Column(db.String(500), nullable=False)


class List_achieves_teams(db.Model):
    id_ach_team = db.Column(db.Integer, primary_key=True)
    name_ach_team = db.Column(db.String(500), nullable=False)
    ach_price = db.Column(db.Integer, nullable=False)


class List_achieves_users(db.Model):
    id_ach = db.Column(db.Integer, primary_key=True)
    name_ach = db.Column(db.String(500), nullable=False)
    ach_price = db.Column(db.Integer, nullable=False)


class Teams_achieves(db.Model):
    id_team = db.Column(db.Integer, db.ForeignKey('teams.id_team'), nullable=False)
    id_ach_team = db.Column(db.Integer, db.ForeignKey('list_achieves_teams.id_ach_team'), nullable=False)
    id_ta = db.Column(db.Integer, primary_key=True)


class Users_achieves(db.Model):
    uid_user = db.Column(db.Integer, db.ForeignKey('users.uid_user'), nullable=False)
    id_ach = db.Column(db.Integer, db.ForeignKey('list_achieves_users.id_ach'), nullable=False)
    id_ua = db.Column(db.Integer, primary_key=True)
