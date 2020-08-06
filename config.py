import os


class Config:
    _user, _password, _host, _database = "root", "password", "localhost", "db_api"
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://{}:{}@{}/{}".format(
        _user, _password, _host, _database
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True
