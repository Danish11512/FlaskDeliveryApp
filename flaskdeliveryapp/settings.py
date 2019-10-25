# -*- coding: utf-8 -*-
"""Application configuration.

Most configuration is set via environment variables.

For local development, use a .env file to set
environment variables.
"""
<<<<<<< HEAD
=======
import os
>>>>>>> 4a790e3ec4a00a3fcbff3ad0e4f39125ce6763e5
from environs import Env

env = Env()
env.read_env()

ENV = env.str("FLASK_ENV", default="production")
DEBUG = ENV == "development"
<<<<<<< HEAD
SQLALCHEMY_DATABASE_URI = env.str("DATABASE_URL")
=======
SQLALCHEMY_DATABASE_URI = (os.environ.get('DEV_DATABASE_URL') or
                               'postgresql://localhost@127.0.0.1:5432/flaskdeliveryapp')
>>>>>>> 4a790e3ec4a00a3fcbff3ad0e4f39125ce6763e5
SECRET_KEY = env.str("SECRET_KEY")
BCRYPT_LOG_ROUNDS = env.int("BCRYPT_LOG_ROUNDS", default=13)
DEBUG_TB_ENABLED = DEBUG
DEBUG_TB_INTERCEPT_REDIRECTS = False
CACHE_TYPE = "simple"  # Can be "memcached", "redis", etc.
SQLALCHEMY_TRACK_MODIFICATIONS = False
WEBPACK_MANIFEST_PATH = "webpack/manifest.json"
