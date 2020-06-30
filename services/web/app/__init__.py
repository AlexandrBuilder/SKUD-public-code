import logging
import os
from logging.handlers import RotatingFileHandler

import flask_excel as excel
from flask import Flask
from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from config import Config

db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
mail = Mail()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    login.login_view = 'auth.login'
    login.login_message = 'Пожалуйста, войдите, чтобы получить доступ к этой странице'
    mail.init_app(app)
    excel.init_excel(app)

    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from app.errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    from app.users import bp as user_bp
    app.register_blueprint(user_bp, url_prefix='')

    from app.cameras import bp as camera_bp
    app.register_blueprint(camera_bp, url_prefix='')

    from app.events import bp as event_bp
    app.register_blueprint(event_bp, url_prefix='')

    from app.report import bp as report_bp
    app.register_blueprint(report_bp, url_prefix='')

    if not app.debug:
        os.mkdir('logs')
        file_handler = RotatingFileHandler('logs/microblog.log', maxBytes=10240, backupCount=10)
        file_handler.setFormatter(
            logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)

    return app


from app import models
