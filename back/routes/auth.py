from back import app, engine
from flask import request, jsonify
from flask_jwt_extended import create_access_token
from werkzeug.security import check_password_hash, generate_password_hash

from back.utils import query_first


@app.route("/login", methods=["POST"])
def login():
    telegram_name = request.json.get("telegram_name", None)
    password = request.json.get("password", None)
    access_token = create_access_token(identity=telegram_name)
    check_password_hash()
    return jsonify(access_token=access_token)


@app.route("/login", methods=["POST"])
def login():
    telegram_name = request.json.get("telegram_name", None)
    password = request.json.get("password", None)
    with engine.connect() as con:
        query_hash = f"""select password
                                   from users
                                   where telegram_name = '{telegram_name}'
                                )"""
        status_value = query_first(query_hash, con)
    if check_password_hash(pwhash=status_value['password'], password=password):
        access_token = create_access_token(identity=telegram_name)
        return jsonify(access_token=access_token)
    else:
        return 'User is not found', 409


@app.route("/reg", methods=["POST"])
def reg():
    req: dict = request.json
    fio = request.json.get("fio")
    telegram_name = req.get("telegram_name")
    password = req.get("password")
    hash_pass = generate_password_hash(password)
    with engine.connect() as con:
        query_req_check = f"""select exists (
                                select
                                from users
                                where telegram_name = '{telegram_name}'
                             )"""
        is_exists: bool = query_first(query_req_check, con)['exists']
    if is_exists:
        return 'User already exists', 409
    with engine.connect() as con:
        query_req = f"""insert into users(fio, hash_pass, telegram_name)
                        values('{fio}', '{hash_pass}', '{telegram_name}')"""
        con.execute(query_req)
    access_token = create_access_token(identity=telegram_name)
    return jsonify(access_token=access_token)
