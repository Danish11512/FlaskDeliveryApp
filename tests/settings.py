"""Settings module for test app."""
ENV = "development"
TESTING = True
<<<<<<< HEAD
SQLALCHEMY_DATABASE_URI = "sqlite://"
=======
SQLALCHEMY_DATABASE_URI = "postgresql://localhost:5432/flaskdeliveryapp"
>>>>>>> 4a790e3ec4a00a3fcbff3ad0e4f39125ce6763e5
SECRET_KEY = "not-so-secret-in-tests"
BCRYPT_LOG_ROUNDS = (
    4
)  # For faster tests; needs at least 4 to avoid "ValueError: Invalid rounds"
DEBUG_TB_ENABLED = False
CACHE_TYPE = "simple"  # Can be "memcached", "redis", etc.
SQLALCHEMY_TRACK_MODIFICATIONS = False
WEBPACK_MANIFEST_PATH = "webpack/manifest.json"
WTF_CSRF_ENABLED = False  # Allows form testing
