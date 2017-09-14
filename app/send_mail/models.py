from .. import db
from datetime import datetime, timedelta

class MailLog(db.Model):
    __tablename__ = 'mail_log'
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(500))
    #message = db.Column(db.String(255))
    sendto = db.Column(db.String(1024))
    remote_addr = db.Column(db.String(64))
    from_app = db.Column(db.String(255))
    send_time = db.Column(db.DateTime, default = datetime.now())
    retry = db.Column(db.Integer, default = 0)

    def __init__(self, **kwargs):
        self.title = kwargs['title']
        self.sendto = kwargs['sendto']
        self.remote_addr = kwargs['remote_addr']
        self.from_app = kwargs['from_app']
