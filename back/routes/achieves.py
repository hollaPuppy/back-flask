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
        result_achieves = con.execute(query_achieves)
        profile_achieve = [row._asdict() for row in result_achieves]
    return jsonify(profile_achieve)


@app.route("/list_achieve_users", methods=["GET"])
def get_user_list_achieve():
    with engine.connect() as con:
        query_user_list_achieve = f"""select id_ach, name_ach, ach_price
                                      from List_achieves_users"""
        result_user_list_achieve = con.execute(query_user_list_achieve)
        user_list_achieve = [row._asdict() for row in result_user_list_achieve]
    return jsonify(user_list_achieve)


@app.route("/list_achieve_teams", methods=["GET"])
def get_teams_list_achieve():
    with engine.connect() as con:
        query_teams_list_achieve = f"""select id_ach_team, name_ach_team, ach_price
                                       from List_achieves_teams"""
        result_teams_list_achieve = con.execute(query_teams_list_achieve)
        teams_list_achieve = [row._asdict()
                              for row in result_teams_list_achieve]
    return jsonify(teams_list_achieve)
