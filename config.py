# -*- coding: utf-8 -*-

# Python imports
from os import getenv
from datetime import timedelta

from dotenv import load_dotenv
load_dotenv()

class Config:
    SECRET_KEY = getenv('SECRET_KEY') or 'EHhEAueAHeuahIAEheAIk'
    PORT = int(getenv('PORT', 5000))
    DEBUG = getenv('DEBUG') or False
    MONGODB_HOST = getenv('MONGODB_URI', "mongodb://localhost:27017/crud_users")
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(
        minutes=int(getenv("JWT_ACCESS_TOKEN_EXPIRES", 60))
    )
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(
        days=int(getenv("JWT_REFRESH_TOKEN_EXPIRES", 30))
    )

class DevelopmentConfig(Config):
    FLASK_ENV = 'development'
    DEBUG = True

class ProdConfig(Config):
    FLASK_ENV = "production"
    DEBUG = False

config = {
    'development': DevelopmentConfig,
    'production': ProdConfig,
    'default': DevelopmentConfig
}

