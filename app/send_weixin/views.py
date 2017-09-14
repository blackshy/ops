import requests
from flask import current_app, request
from flask_restful import Api, Resource, reqparse
from threading import Thread 
from . import send_weixin
from .. import db
from .models import WeixinLog
import time
import json
import textwrap

import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )

app = current_app._get_current_object()
api = Api(send_weixin)

@api.resource('/')
class SendWeixin(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('title',   type = str, location = ['headers', 'values', 'json'], required = True)
        self.reqparse.add_argument('message', type = str, location = ['headers', 'values', 'json'], required = True)
        self.reqparse.add_argument('sendto',  type = str, location = ['headers', 'values', 'json'], required = True)
        self.reqparse.add_argument('type',    type = str, location = ['headers', 'values', 'json'], default = 'text')
        self.reqparse.add_argument('app',     type = str, location = ['headers', 'values', 'json'], default = 'common')
        self.args = self.reqparse.parse_args()
        self.remote_addr = request.remote_addr
        
        self.send_message_url = app.config['WEIXIN_SEND_URL']
        self.gettoken_url = app.config['WEIXIN_GETTOKEN_URL']
        self.gettoken_content = {
                'corpid': app.config['WEIXIN_CORPID'],
                'corpsecret': app.config['WEIXIN_SECRET']
                }
        self.token_cache = {
                'token': '',
                'expires_time': 0
                }

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
                #server_users_json = self.get_server_users(server_ip)
                append_server_description = "\nServer Description: " + server_info_json['description'].encode('utf-8')
                message += append_server_description
                #append_server_users = "\nServer Users: "
                #for item in server_users_json:
                #    #append_server_users += '\nuser_name: ' + item['username'] + ', expires_time: ' + item['expires_time'] + ', sudo: ' + item['sudo']
                #    append_server_users += item['username'] + ', '
                #append_server_users = append_server_users.strip(', ').encode('utf-8')
                #message += append_server_users
            except:
                print subject
                pass
        recipients = args['sendto'].replace(';', '|')
        weixin_type  = args['type']

        each_message_len = 1999
        message_list = textwrap.wrap(message, each_message_len, replace_whitespace = False)

        weixin_token = self.get_token()

        for msg in message_list:
            full_message = {
                    "touser": recipients,
                    "agentid": 6,
                    "msgtype": weixin_type,
                    "text": {
                        "content": subject + '\n' + msg
                        },
                    "safe": 0
                    }
            result = self.send_async_weixin(weixin_token, full_message)

        weixin_log = WeixinLog(title = subject, sendto = recipients, remote_addr = self.remote_addr, from_app = self.args['app'])
        db.session.add(weixin_log)
        db.session.commit()
        return 'OK'

    def async(f):
        def wrapper(*args, **kwargs):
            thr = Thread(target = f, args = args, kwargs = kwargs)
            thr.start()
        return wrapper
    
    @async
    def send_async_weixin(self, token, message):
        """Background task to send an weixin."""
        with app.app_context():
            result = self.send_by_requests(token, message)
        return result

    def get_token(self):
        current_time = int(time.time())
        if (current_time > self.token_cache['expires_time']):
            r = requests.get(self.gettoken_url, params = self.gettoken_content)
            self.token_cache['token'] = r.json()['access_token']
            self.token_cache['expires_time'] = (current_time + int(r.json()['expires_in']) - 300)
        result = self.token_cache['token']
        return result


    def send_by_requests(self, token, message):
        url = self.send_message_url + token
        data = json.dumps(message, ensure_ascii=False)
        r = requests.post(url, data = data)
        result = r.json()
        return result
