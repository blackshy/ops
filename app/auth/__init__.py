from flask import Blueprint

#auth = Blueprint('auth', __name__, template_folder='templates')
auth = Blueprint('auth', __name__)

from . import views
