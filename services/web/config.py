import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 465)
    MAIL_USE_SSL = os.environ.get('MAIL_USE_SSL') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    USERS_PER_PAGE = 15
    EVENTS_PER_PAGE = 15
    SUCCESS_FLASH = 'success'
    ERROR_FLASH = 'danger'
    URL_VECTOR_SERVER = 'https://dispace.edu.nstu.ru/asdasdas'
    STATIC_DIR = os.path.join(basedir, 'app/static')
    UPLOAD_AVATAR_FOLDER = 'uploads/avatars'
    NO_IMAGE_FILE = 'uploads/defaults/no-image.png'
