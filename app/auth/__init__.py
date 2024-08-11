from flask import Blueprint, current_app

auth_bp = Blueprint('auth', __name__)

from app.auth import auth_routes
