from os import environ, path

basedir = path.abspath(path.dirname(__file__))


class Config:
    SECRET_KEY = environ.get('SECRET_KEY') or 'nobody-gonna-guess-it'
    STATIC_PATH = './app/static'
    DEBUG = False
