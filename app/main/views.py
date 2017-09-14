from flask import render_template, redirect, url_for, abort, flash, request,\
        current_app, make_response
from flask_login import login_required, current_user
from . import main
#from .forms import 
from .. import db
from ..models import Permission, Role, User

from ..decorators import admin_required, permission_required


@main.route('/')
@login_required
def index():
    if current_user.is_authenticated:
        return render_template('index.html')
