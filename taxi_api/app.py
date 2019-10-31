from flask import Flask
from flask_pymongo import PyMongo


app = Flask(__name__)
# app.secret_key = "secret key"

mongo0 = PyMongo(app, uri = 'mongodb://localhost:27018/discovery_database')
mongo = PyMongo(app, uri = 'mongodb://localhost:27018/demo_api')
