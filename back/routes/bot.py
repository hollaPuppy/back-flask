from back import app, engine
from flask import jsonify


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
