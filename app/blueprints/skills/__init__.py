from flask import Blueprint

bp = Blueprint('skills', __name__)


from app.blueprints.skills import routes