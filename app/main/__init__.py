from flask import Blueprint, current_app


bp = Blueprint('main', __name__)

from app.main import routes
