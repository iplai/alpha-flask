import os

from flask import Flask, Blueprint
from flask_moment import Moment
from flask_login import LoginManager
from flask_principal import Principal
from flask_bootstrap import Bootstrap
from flask_mongoengine import MongoEngine

from app.config import Config

BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
TEMPLATE_PATH = os.path.join(BASE_DIR, 'templates').replace('\\', '/')
STATIC_PATH = os.path.join(BASE_DIR, 'assets').replace('\\', '/')

app = Flask(__name__, template_folder=TEMPLATE_PATH, static_folder=STATIC_PATH)
app.config.from_object(Config)
db = MongoEngine(app)
moment = Moment(app)

login_manager = LoginManager(app)
login_manager.session_protection = 'strong'
login_manager.login_view = 'app.login'

principals = Principal(app)

bootstrap = Bootstrap(app)

blueprint = Blueprint('app', __name__)
