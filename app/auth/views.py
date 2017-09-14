from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, logout_user, login_required, \
        current_user
from . import auth
from .. import db
from ..models import User
from .forms import LoginForm


#@auth.before_app_request
#def before_request():
#    if current_user.is_authenticated:
#        current_user.ping()
#        if request.endpoint \
#                and request.endpoint[:5] != 'auth.' \
#                and request.endpoint != 'static':
#            return redirect(url_for('auth.login'))

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.rember_me.data)
            return redirect(request.args.get('next') or url_for('main.index'))
        flash('Invalid username or password.')
    return render_template('auth/login.html', form=form)

@auth.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.index'))
