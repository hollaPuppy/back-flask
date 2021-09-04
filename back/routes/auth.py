from back import app, engine
from flask import request, jsonify
from flask_jwt_extended import create_access_token
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
    with engine.connect() as con:
        query_req = f"""insert into users(fio, hash_pass, telegram_name)
                        values('{fio}', '{hash_pass}', '{telegram_name}')"""
        con.execute(query_req)
    access_token = create_access_token(identity=telegram_name)
    return jsonify(access_token=access_token)
