from flask import Blueprint
from .. import db

send_mail = Blueprint('send_mail', __name__)

from . import views
from .views import SendEmail
db.create_all()
