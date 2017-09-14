from flask import Blueprint
from .. import db

zbx = Blueprint('zbx', __name__, template_folder='templates')

from . import views
from .views import Zabbix
#db.create_all()
