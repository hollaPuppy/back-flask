from datetime import datetime
from back.utils import query_all, query_first
from back import app, engine
from flask import jsonify


@app.route("/get_status/<telegram_name>", methods=["GET"])
def get_status_user(telegram_name):
    with engine.connect() as con:
        query_status = f"""select status
                           from users
                           where telegram_name = '{telegram_name}'"""
        status_value = query_all(query_status, con)
    return jsonify(status_value)


@app.route("/get_mes", methods=["GET"])
def get_mes():
    with engine.connect() as con:
        query_status = f"""select text_mes
                            from messages
                            where date(date_to_send) = '{datetime.today().strftime('%Y-%m-%d')}'
                        """
        status_value = query_first(query_status, con)
    return jsonify(status_value)
