from flask import request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

from back import app, db, engine, api

from werkzeug.security import generate_password_hash

from flask_pydantic_spec import Response, Request
from back.models import Profile, Message


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
    req: dict = request.json
    fio = req.get("fio")
    id_team = req.get("id_team")
    telegram_name = req.get("telegram_name")
    current_user = get_jwt_identity()
    with engine.connect() as con:
        query_sql = f"""update users set
                        fio = '{fio}', telegram_name = '{telegram_name}', id_team = '{id_team}' 
                        where telegram_name={current_user}"""
        con.execute(query_sql)
    return 'Profile update complete successfully'


@app.route("/profile/<telegram_name>", methods=["GET"])
@jwt_required()
def get_profile(telegram_name):
    current_user = get_jwt_identity()
    with engine.connect() as con:
        query_profile = f"""select u.fio, u.img, u.telegram_name, u.balance, t.team_name
                        from users u
                        left join teams t 
                        on t.id_team=u.id_team
                        where telegram_name='{current_user}'"""
        result_profile = con.execute(query_profile)
        profile_info = [row._asdict() for row in result_profile][0]
        query_achieves = f"""select lau.name_ach, lau.ach_price
                         from users u
                         join users_achieves ua
                         on ua.uid_user = u.uid_user
                         join list_achieves_users lau
                         on lau.id_ach = ua.id_ach"""
        result_achieves = con.execute(query_achieves)
        profile_achieve = [row._asdict() for row in result_achieves]
        profile_info['achivements'] = profile_achieve
    return jsonify(profile_info)


@app.route("/all_achieves", methods=["GET"])
@jwt_required()
def get_achieves():
    with engine.connect() as con:
        query_achieves = f"""select name_ach, ach_price
                        from list_achieves_users"""
        result_achieves = con.execute(query_achieves)
        all_achieves = [row._asdict() for row in result_achieves]
    return jsonify(all_achieves)


@app.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200


@app.route('/')
def index():
    return 'Index Page'


@app.route("/team_balance/<id_team>", methods=["GET"])
@jwt_required()
def get_team_id(id_team):
    with engine.connect() as con:
        query_sql = f"""select sum(balance)
                        from users 
                        where id_team={id_team}"""
        result = con.execute(query_sql)
        team_sum = [row._asdict() for row in result][0]
    return team_sum


@app.route("/team_info/<id_team>", methods=["GET"])
@jwt_required()
def get_team_info(id_team):
    with engine.connect() as con:
        query_sql = f"""select sum(u.balance), t.team_name
                        from users u
                        join teams t 
                        on t.id_team=u.id_team
                        where t.id_team={id_team}
                        group by t.team_name"""
        result = con.execute(query_sql)
        team_sum = [row._asdict() for row in result][0]
    return team_sum


@app.route("/team_enter/<id_team>", methods=["PUT"])
@jwt_required()
def get_team_enter(id_team):
    current_user = get_jwt_identity()
    with engine.connect() as con:
        query_enter = f"""update users
                        set id_team={id_team}
                        where telegram_name='{current_user}'"""
        con.execute(query_enter)
    return 'Update status complete successfully'


@app.route("/upd_status/<status>", methods=["PUT"])
@jwt_required()
def update_status(status):
    current_user = get_jwt_identity()
    with engine.connect() as con:
        query_upd = f"""update users
                        set status={status}
                        where telegram_name='{current_user}'"""
        con.execute(query_upd)
    return 'Enter to team complete successfully'


@app.route("/team_list", methods=["GET"])
@jwt_required()
def get_team_list():
    with engine.connect() as con:
        query_sql = f"""select teams.team_name, sum(users.balance)
                        from teams 
                        join users  
                        on users.id_team=teams.id_team 
                        group by teams.team_name"""
        result = con.execute(query_sql)
        team_list = [row._asdict() for row in result]
    return jsonify(team_list)


@app.route("/user_list", methods=["GET"])
@jwt_required()
def get_user_list():
    with engine.connect() as con:
        query_sql = f"""select users.telegram_name, users.img, users.balance, teams.team_name
                        from users 
                        left join teams
                        on teams.id_team=users.id_team
                        order by users.balance ASC"""
        result = con.execute(query_sql)
        user_list = [row._asdict() for row in result]
    return jsonify(user_list)


@app.route("/list_achieve_users", methods=["GET"])
@jwt_required()
def get_user_list_achieve():
    with engine.connect() as con:
        query_sql = f"""select id_ach, name_ach, ach_price
                        from List_achieves_users"""
        result = con.execute(query_sql)
        user_list = [row._asdict() for row in result]
    return jsonify(user_list)


@app.route("/list_achieve_teams", methods=["GET"])
@jwt_required()
def get_teams_list_achieve():
    with engine.connect() as con:
        query_sql = f"""select id_ach_team, name_ach_team, ach_price
                        from List_achieves_teams"""
        result = con.execute(query_sql)
        user_list = [row._asdict() for row in result]
    return jsonify(user_list)


@app.route("/get_status/<telegram_name>", methods=["GET"])
def get_status_user(telegram_name):
    with engine.connect() as con:
        query_status = f"""select status
                        from users
                        where telegram_name = '{telegram_name}'"""
        result_status = con.execute(query_status)
        status_value = [row._asdict() for row in result_status]
    return jsonify(status_value)


@app.route("/get_mes/<status>", methods=["GET"])
def get_mes(status):
    with engine.connect() as con:
        query_status = f"""select id_mes, date_to_send, text_mes
                        from messages
                        where status = '{status}'"""
        result_status = con.execute(query_status)
        status_value = [row._asdict() for row in result_status]

    return jsonify(status_value)


@app.route("/get-achieve/<telegram_name>", methods=["GET"])
def get_achieve_user(telegram_name):
    with engine.connect() as con:
        query_achieves = f"""select lau.name_ach, lau.ach_price
                         from users u
                         join users_achieves ua
                         on ua.uid_user = u.uid_user
                         join list_achieves_users lau
                         on lau.id_ach = ua.id_ach
                         where telegram_name='{telegram_name}'"""
        result_achieves = con.execute(query_achieves)
        profile_achieve = [row._asdict() for row in result_achieves]
    return jsonify(profile_achieve)


@app.route("/get-list-achieve-user", methods=["GET"])
def get_list_achieve_user():
    with engine.connect() as con:
        query_achieves = f"""select name_ach, ach_price
                         from list_achieves_users"""
        result_achieves = con.execute(query_achieves)
        profile_achieve = [row._asdict() for row in result_achieves]
    return jsonify(profile_achieve)


@app.route("/get-list-achieve-team", methods=["GET"])
def get_list_achieve_team():
    with engine.connect() as con:
        query_achieves_team = f"""select name_ach_team, ach_price
                         from list_achieves_teams"""
        result_achieves_team = con.execute(query_achieves_team)
        profile_achieve_team = [row._asdict() for row in result_achieves_team]
    return jsonify(profile_achieve_team)
