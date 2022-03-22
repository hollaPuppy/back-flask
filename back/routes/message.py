from back.utils import query_all
from back import app, engine
from flask import jsonify
from flask_socketio import SocketIO, send


@socketio.on('message')
def handleMessage(msg):
    print('Message:' + msg)
    send(msg, broadcast=True)

