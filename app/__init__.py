from flask import Flask
from flask_bootstrap import Bootstrap 
from flask_mail import Mail
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy 
from flask_login import LoginManager
from flask_pagedown import PageDown
from config import config

login_manager = LoginManager()
bootstrap = Bootstrap()
mail = Mail()
moment = Moment()
db = SQLAlchemy()
pagedown = PageDown()

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'

def create_app(config_name):
    app = Flask(__name__)
    app.debug = True
    app.config.from_object(config[config_name]) 
    config[config_name].init_app(app)
        
    bootstrap.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    pagedown.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    from .assets import assets as assets_blueprint 
    app.register_blueprint(assets_blueprint, url_prefix='/assets')

    #from .send_mail import send_mail as mail_blueprint
    #app.register_blueprint(mail_blueprint, url_prefix='/mail')

    #from .send_weixin import send_weixin as weixin_blueprint
    #app.register_blueprint(weixin_blueprint, url_prefix='/weixin')
    #
    #from .zabbix import zbx as zabbix_blueprint
    #app.register_blueprint(zabbix_blueprint, url_prefix='/zabbix')
    
    return app
