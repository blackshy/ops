import datetime
from datetime import date, timedelta
from flask_wtf import Form
import wtforms
from wtforms.validators import Required, InputRequired, Boolean
#from flask_admin.form import DateTimeField, DatePickerWidget, DateTimePickerWidget

import sys
reload(sys)
sys.setdefaultencoding("utf-8")

class AdminUserCreateForm(Form):
    username = TextField('Username', [InputRequired()])
    password = PasswordField('Password', [InputRequired()])
    admin = BooleanField('Is Admin ?')

class AdminUserUpdateForm(Form):
    username = TextField('Username', [InputRequired()])
    admin = BooleanField('Is Admin ?')
