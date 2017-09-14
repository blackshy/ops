from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import Required, Length, Email, Regexp, EqualTo
from wtforms import ValidationError
from ..models import User
import sys
reload(sys)
sys.setdefaultencoding("utf-8")


class LoginForm(FlaskForm):
    #email = StringField('Email', validators=[Required(), Length(1, 64), Email()])
    username = StringField('User', validators=[Required(), Length(1, 64)])
    password = PasswordField('Password', validators=[Required()])
    rember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log In')
