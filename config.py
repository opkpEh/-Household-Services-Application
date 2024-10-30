import os

class Config:
    SECRET_KEY = 'dev'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///household_services.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False