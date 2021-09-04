from flask import request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

from back import app, db, engine
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
    with engine.connect() as con:
        query_sql = f"""insert into users(fio, hash_pass, telegram_name)
                        values('{fio}', '{hash_pass}', '{telegram_name}')
                    """
        con.execute(query_sql)
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


@app.route("/profile/<telegram_name>", methods=["GET"])
@jwt_required()
def get_profile(telegram_name):
    users = Users.query.filter_by(telegram_name=telegram_name).one()
    return {"telegram_name": users.telegram_name, "fio": users.fio, "img": users.img, "balance": users.balance, "id_team": users.id_team, "status": users.status}


@app.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200


@app.route('/')
def index():
    return 'Index Page'


@app.route("/team_balance/<id_team>", methods=["GET"])
def get_team_id(id_team):
    with engine.connect() as con:
        query_sql = f"""select sum(balance)
                        from users 
                        where id_team={id_team}"""
        result = con.execute(query_sql)
        team_sum = [row._asdict() for row in result][0]
    return team_sum


@app.route("/team_enter/<id_team>", methods=["PUT"])
@jwt_required()
def get_team_enter(id_team):
    current_user = get_jwt_identity()
    with engine.connect() as con:
        query_sql = f"""update users
                        set id_team={id_team}
                        where telegram_name={current_user}"""
    return 'well'
