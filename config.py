import os


class Config(object):
    PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
    SECRET_KEY = 'ix5n{z`jp9Tv81r{EB9r&AU-Ey9J(BC.'
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = 'toor'
    MYSQL_DB = 'computer_monitor'
    API_KEY = 'vpNbIfJvGrYjSWe44TLFfSIRFfYsP5Wa'
    #DATABASE_FILE = "sqlite:///{}".format(os.path.join(PROJECT_DIR, "app.db"))
    SQLALCHEMY_DATABASE_URI = 'mysql://' + MYSQL_USER + ':' + MYSQL_PASSWORD + '@' + MYSQL_HOST + '/' + MYSQL_DB
    # SQLALCHEMY_DATABASE_URI = DATABASE_FILE
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    BUILD_ENV = ['development', 'production']
    FLASK_ENV = BUILD_ENV[0]
    if FLASK_ENV == BUILD_ENV[0]:
        DEBUG = True
    else:
        DEBUG = False
