import os
from datetime import timedelta

from flask import Flask
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
#from flask_cors import CORS
from back.settings import DATABASE_URL

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://faozuispekgops:49e44fdedf916d54c5d562385a7677a6f387af7111403befac06fa0b2f96c73b@ec2-176-34-116-203.eu-west-1.compute.amazonaws.com:5432/d1gec1g9j9v7sr'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(days=300)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=30)

#CORS(app)
db = SQLAlchemy(app)
engine = db.create_engine('postgresql://faozuispekgops:49e44fdedf916d54c5d562385a7677a6f387af7111403befac06fa0b2f96c73b@ec2-176-34-116-203.eu-west-1.compute.amazonaws.com:5432/d1gec1g9j9v7sr',{})
app.config["JWT_SECRET_KEY"] = "aboba"
jwt = JWTManager(app)


from back import models, routes
