from flask import Flask
from .mongo import MongoDB

app = Flask(__name__)
mongo = MongoDB()

app.config.from_object('config')

from app import views
