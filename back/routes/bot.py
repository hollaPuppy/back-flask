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
        status_value = query_first(query_status, con)
    return jsonify(status_value)


@app.route("/get_mes/<status>", methods=["GET"])
def get_mes(status):
    with engine.connect() as con:
        query_status = f"""select text_mes
                            from messages
                            where date(date_to_send) = '{datetime.today().strftime('%Y-%m-%d')}'
                            and status={status}
                        """
        status_value = query_first(query_status, con)
    return jsonify(status_value)


@app.route("/check_user/<telegram_name>", methods=["GET"])
def check_user(telegram_name):
        with engine.connect() as con:
            query_req_check = f"""select exists (
                                       select
                                       from users
                                       where telegram_name = '{telegram_name}'
                                    )"""
            is_exists: bool = query_first(query_req_check, con)['exists']
        if not is_exists:
            return 'User not exists', 409
        return 'User exists'
