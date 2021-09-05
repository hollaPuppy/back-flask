from back.utils import query_all
from back import app, engine
from flask import jsonify

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
        profile_achieve = query_all(query_achieves, con)
    return jsonify(profile_achieve)


@app.route("/list_achieve_users", methods=["GET"])
def get_user_list_achieve():
    with engine.connect() as con:
        query_user_list_achieve = f"""select id_ach, name_ach, ach_price
                                      from list_achieves_users"""
        user_list_achieve = query_all(query_user_list_achieve, con)
    return jsonify(user_list_achieve)


@app.route("/list_achieve_teams", methods=["GET"])
def get_teams_list_achieve():
    with engine.connect() as con:
        query_teams_list_achieve = f"""select id_ach_team, name_ach_team, ach_price
                                       from list_achieves_teams"""
        teams_list_achieve = query_all(query_teams_list_achieve, con)
    return jsonify(teams_list_achieve)
