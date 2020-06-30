from flask import Blueprint

bp = Blueprint('cameras', __name__)

from app.cameras import routes
