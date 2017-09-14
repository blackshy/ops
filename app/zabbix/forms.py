import datetime
from datetime import date, timedelta
from flask_wtf import Form
import wtforms
from wtforms.validators import Required, InputRequired
#from flask_admin.form import DateTimeField, DatePickerWidget, DateTimePickerWidget

import sys
reload(sys)
sys.setdefaultencoding("utf-8")

class DateRangeForm(Form):
    #end_time = wtforms.DateField('End at', [wtforms.validators.required()], format='%Y-%m-%d')
    _today = date.today()
    _yesterday = date.today() - timedelta(7)
    today_str = _today.strftime('%Y-%m-%d')
    yesterday_str = _yesterday.strftime('%Y-%m-%d')
    start_time = wtforms.StringField('Start', default=yesterday_str, validators=[InputRequired()])
    end_time = wtforms.StringField('End', default=today_str, validators=[InputRequired()])
    hosts_list = [
            '10.0.8.247',
            '10.0.8.248',
            '10.0.8.249',
            '10.0.8.250',
            '10.0.8.251',
            '10.0.8.252',
            '10.0.9.251',
            '10.0.9.252'
            ]
    hosts_choices_list = []
    hosts_choices_list.append((','.join(hosts_list), 'All_kvm_hosts'))
    for host in hosts_list:
        hosts_choices_list.append((host, host))
    print hosts_choices_list
    hosts = wtforms.SelectField('Hosts', choices=hosts_choices_list)
    submit = wtforms.SubmitField('Submit')
