from flask import request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

from back import app, db
from back.models import Users, Teams, List_achieves_teams, List_achieves_users, Teams_achieves, Users_achieves

from werkzeug.security import generate_password_hash


@app.route("/login", methods=["POST"])
def login():
    telegram_name = request.json.get("telegram_name", None)
    password = request.json.get("password", None)

    access_token = create_access_token(identity=telegram_name)
    return jsonify(access_token=access_token)


@app.route("/reg", methods=["POST"])
def reg():
    req: dict = request.json
    fio = request.json.get("fio")
    telegram_name = req.get("telegram_name")
    password = req.get("password")
    hash_pass = generate_password_hash(password)
    user = Users(fio=fio, hash_pass=hash_pass, telegram_name=telegram_name)
    db.session.add(user)
    db.session.commit()
    access_token = create_access_token(identity=telegram_name)
    return jsonify(access_token=access_token)


@app.route("/profile-switch", methods=["PUT"])
@jwt_required()
def put_profile():
    current_user = get_jwt_identity()
    req: dict = request.json
    username = req.get("username")
    email = req.get("email")
    password = req.get("password")
    hash_pass = generate_password_hash(password)
    user = Users(username=username, hash_pass=hash_pass, email=email)
    db.session.add(user)
    db.session.commit()


@app.route("/profile/<username>", methods=["GET"])
@jwt_required()
def get_profile(username):
    users = Users.query.filter_by(username=username).one()
    return {"username": users.username, "email": users.email, "img": users.img, "first_name": users.first_name, "second_name": users.second_name}


@app.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200


@app.route('/')
def index():
    return 'Index Page'



