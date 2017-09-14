from flask import Blueprint
from .. import db

send_weixin = Blueprint('send_weixin', __name__)

from . import views
from .views import SendWeixin
db.create_all()
