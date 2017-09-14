#!/usr/bin/env python
# coding: utf8

''' to send zabbix alert mail '''
from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.utils import parseaddr, formataddr
import smtplib
import requests
import json
import getopt
import sys

class send_mail(object):
    def __init__(self):
        #self.api_url = 'http://10.0.8.45:5000/mail/'
        self.api_url = 'http://127.0.0.1:5000/mail/'
        self.headers = { 'Content-Type': 'Application/json' }
        self.title = ''
        self.message = ''
        self.sendto = ''

    def send_mail_api(self):
        data = {
                'title': self.title + '( from api)',
                'message': self.message,
                'sendto': self.sendto,
                'app': 'zabbix'
                }
        r = requests.post(self.api_url, data = json.dumps(data), headers = self.headers, timeout=10)
        return r.status_code

    def send_mail_local(self):
      mail_host = ''
      mail_user = 'no-reply@blackshy.com'
      mail_pass = ''
      debug = 0

      msg = MIMEText(self.message.replace('\n', '<br>'), _subtype='html', _charset='utf-8')
      me = mail_user
      msg['To'] = self.sendto
      msg['From'] = mail_user
      msg['Subject'] = self.title + '( from local)'
      try:
        s = smtplib.SMTP()
        if debug:
            s.set_debuglevel(1)
        s.connect(mail_host)
        s.starttls()
        s.login(mail_user, mail_pass)
        s.sendmail(me, self.sendto, msg.as_string())
        s.close()
        return True
      except Exception, e:
        print str(e)
        return False

    def Usage(self):
        print ''
        print '    -t | --title=           mail title'
        print '    -m | --message=         mail message'
        print '    -s | --sendto=          send user list [ example: user1@blackshy.com;user2@blackshy.com ]'
        print '    --help                  print this help message'
        print ''

    def get_opts(self):
        try:
            opts , args = getopt.getopt(sys.argv[1:],"vh:t:m:s:", ["help","title=","message=","sendto="])
        except getopt.GetoptError, err:
            print str(err)
            self.Usage()
            sys.exit(2)

        for op , value in opts:
            if op in ("-t","--title"):
                self.title = value
            elif op in ('-m',"--message"):
                self.message = value
            elif op in ('-s',"--sendto"):
                self.sendto = value
            elif op == "--help":
                self.Usage()
                sys.exit(3)
            else:
                print 'unhandled option'

if __name__ == '__main__':
    mail = send_mail()
    mail.get_opts()
    result = 400
    try:
        result = mail.send_mail_api()
    finally:
        if result != 200:
            print 'Can not access mail api!'
            mail.send_mail_local()
