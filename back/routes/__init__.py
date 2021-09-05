from back.utils import query_all
from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from back import app, engine


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


@app.route("/user_list", methods=["GET"])
@jwt_required()
def get_user_list():
    with engine.connect() as con:
        query_user_list = f"""select users.telegram_name, users.img, users.balance, teams.team_name
                              from users 
                              left join teams
                              on teams.id_team=users.id_team
                              order by users.balance ASC"""
        user_user_list = query_all(query_user_list, con)
    return jsonify(user_user_list)
