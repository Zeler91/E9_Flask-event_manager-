from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CsrfProtect

from config import Config

from werkzeug.debug import DebuggedApplication

import os
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.debug = True

    if app.debug:
        app.wsgi_app = DebuggedApplication(app.wsgi_app, evalex=True)

    return app

app = create_app()
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
bcrypt = Bcrypt(app)

from app import routes, models, forms

db.create_all()
