import requests
from flask import current_app, request
from flask_restful import Api, Resource, reqparse
from flask_mail import Mail, Message
from threading import Thread 
from . import send_mail
from .. import mail, db
from .models import MailLog

import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )

app = current_app._get_current_object()
api = Api(send_mail)

@api.resource('/')
class SendEmail(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('title',   type = str, location = ['headers', 'values', 'json'], required = True)
        self.reqparse.add_argument('message', type = str, location = ['headers', 'values', 'json'], required = True)
        self.reqparse.add_argument('sendto',  type = str, location = ['headers', 'values', 'json'], required = True)
        self.reqparse.add_argument('type',    type = str, location = ['headers', 'values', 'json'], default = 'html')
        self.reqparse.add_argument('app',     type = str, location = ['headers', 'values', 'json'], default = 'common')
        self.args = self.reqparse.parse_args()
        self.remote_addr = request.remote_addr

    def get(self):
        return self.send()

    def post(self):
        return self.send()

    def get_server_description(self, ip):
        r = requests.get(app.config['SERVER_DETAIL_API_URL'] + ip)
        result = r.json()
        return result

    def get_server_users(self, ip):
        r = requests.get(app.config['SERVER_USER_API_URL'] + ip)
        result = r.json()
        return result

    def send(self):
        args = self.args
        subject = args['title']
        message = args['message']
        if 'zabbix' in args['app']:
            try:
                server_ip = subject.split(':')[1]
                server_info_json = self.get_server_description(server_ip)
                server_users_json = self.get_server_users(server_ip)
                append_server_description = "\nServer Description: " + server_info_json['description'].encode('utf-8')
                message += append_server_description
                append_server_users = "\nServer Users: "
                for item in server_users_json:
                    #append_server_users += '\nuser_name: ' + item['username'] + ', expires_time: ' + item['expires_time'] + ', sudo: ' + item['sudo']
                    append_server_users += item['username'] + ', '
                append_server_users = append_server_users.strip(', ').encode('utf-8')
                message += append_server_users
            except:
                print subject
                pass
        recipients = args['sendto'].split(';')
        mail_type  = args['type']
        msg = Message(subject, recipients = recipients)
        if 'html' in mail_type:
            html_message = message.replace(' ', '&nbsp')
            msg.html = html_message.replace('\n','<br>')
        else:
            msg.body = message
        msg.charset = 'UTF-8'
        result = self.send_async_email(msg)
        mail_log = MailLog(title = subject, sendto = ';'.join(recipients).strip(';'), remote_addr = self.remote_addr, from_app = self.args['app'])
        db.session.add(mail_log)
        db.session.commit()
        return 'OK'

    def async(f):
        def wrapper(*args, **kwargs):
            thr = Thread(target = f, args = args, kwargs = kwargs)
            thr.start()
        return wrapper
    
    @async
    def send_async_email(self, msg):
        """Background task to send an email with Flask-Mail."""
        with app.app_context():
            result = mail.send(msg)
            print result
