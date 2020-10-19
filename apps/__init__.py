# -*- coding: utf-8 -*-

from flask import Flask
from config import config

from apps.api import configure_api
from apps.db import db
from apps.jwt import configure_jwt

from dotenv import load_dotenv
load_dotenv()

def create_app(config_name):
    app = Flask('crud_users')
    app.config.from_object(config[config_name])

    # setting MongoEngine
    db.init_app(app)

    configure_jwt(app)

    configure_api(app)
    
    return app

