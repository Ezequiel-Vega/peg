from flask import Blueprint

team_leader_bp : Blueprint = Blueprint("team_leader", __name__, template_folder='templates/team_leader')

from . import routes
