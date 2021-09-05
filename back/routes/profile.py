from back import app, engine
from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity


@app.route("/profile-switch", methods=["PUT"])
@jwt_required()
def put_profile():
    req: dict = request.json
    fio = req.get("fio")
    id_team = req.get("id_team")
    telegram_name = req.get("telegram_name")
    current_user = get_jwt_identity()
    with engine.connect() as con:
        query_put_profile = f"""update users
                                set
                                    fio = '{fio}', 
                                    telegram_name = '{telegram_name}', 
                                    id_team = '{id_team}' 
                                where telegram_name={current_user}"""
        con.execute(query_put_profile)
    return 'Profile update complete successfully'


@app.route("/profile/<telegram_name>", methods=["GET"])
@jwt_required()
def get_profile(telegram_name):
    current_user = get_jwt_identity()
    with engine.connect() as con:
        query_profile = f"""select u.fio, u.img, u.telegram_name, 
                                u.balance, t.team_name
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
