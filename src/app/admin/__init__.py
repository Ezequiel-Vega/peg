from flask import Blueprint

admin_bp : Blueprint = Blueprint("admin", __name__, template_folder='templates/admin')

from . import routes
