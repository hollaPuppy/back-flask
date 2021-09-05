import os
from datetime import timedelta

from flask import Flask
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from back.settings import DATABASE_URL
from flask_pydantic_spec import FlaskPydanticSpec, Response

app = Flask(__name__)
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(days=30)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=30)

CORS(app)
db = SQLAlchemy(app)
engine = db.create_engine(DATABASE_URL,{})
app.config["JWT_SECRET_KEY"] = "aboba"
jwt = JWTManager(app)


Response('HTTP_200') # equals to Response(HTTP_200=None)

from back import routes
from back.routes import achieves, auth, bot, team, profile
