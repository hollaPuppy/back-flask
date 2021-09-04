from back import app, engine
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import jsonify


@app.route("/team_balance/<id_team>", methods=["GET"])
@jwt_required()
def get_team_sum(id_team):
    with engine.connect() as con:
        query_sum = f"""select sum(balance)
                        from users 
                        where id_team={id_team}"""
        result_sum = con.execute(query_sum)
        team_sum = [row._asdict() for row in result_sum][0]
    return team_sum


@app.route("/team_info/<id_team>", methods=["GET"])
@jwt_required()
def get_team_info(id_team):
    with engine.connect() as con:
        query_team_info = f"""select sum(u.balance), t.team_name
                              from users u
                              join teams t 
                              on t.id_team=u.id_team
                              where t.id_team={id_team}
                              group by t.team_name"""
        result_team_info = con.execute(query_team_info)
        team_info = [row._asdict() for row in result_team_info][0]
    return team_info


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


@app.route("/team_list", methods=["GET"])
@jwt_required()
def get_team_list():
    with engine.connect() as con:
        query_team_list = f"""select teams.team_name, sum(users.balance)
                              from teams 
                              join users  
                              on users.id_team=teams.id_team 
                              group by teams.team_name"""
        result_team_list = con.execute(query_team_list)
        team_list = [row._asdict() for row in result_team_list]
    return jsonify(team_list)
