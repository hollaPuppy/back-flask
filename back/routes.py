from flask import request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

from back import app, db
from back.models import News, Users

from werkzeug.security import generate_password_hash


@app.route("/login", methods=["POST"])
def login():
    username = request.json.get("username", None)
    password = request.json.get("password", None)

    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token)


@app.route("/reg", methods=["POST"])
def reg():
    req: dict = request.json
    username = req.get("username")
    email = req.get("email")
    password = req.get("password")
    hash_pass = generate_password_hash(password)
    user = Users(username=username, hash_pass=hash_pass, email=email)
    db.session.add(user)
    db.session.commit()
    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token)


@app.route("/profile", methods=["PUT"])
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


@app.route("/add_news", methods=["POST"])
def add_news():
    req: dict = request.json
    title = req.get("title")
    text = req.get("text")
    new = News(title=title, text=text)
    db.session.add(new)
    db.commit()


@app.route('/news', methods=["GET"])
def get_news():
    news = News.query.all()
    news_list = []
    for _ in news:
        news_list.append({"title": news.title, "text": news.text, "img": news.img})
    return news_list


@app.route('/news/<uid_news>', methods=["GET"])
def get_new_one(uid_news):
    news = News.filter_by(uid_news=uid_news).one()
    return {"title": news.title, "text": news.text, "img": news.img}


@app.route('/hello')
def hello():
    return 'Hello, World'
