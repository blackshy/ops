from .. import db
from datetime import datetime, timedelta

class WeixinLog(db.Model):
    __tablename__ = 'weixin_log'
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(500))
    sendto = db.Column(db.String(1024))
    remote_addr = db.Column(db.String(64))
    from_app = db.Column(db.String(255))
    send_time = db.Column(db.DateTime, default = datetime.now())
    retry = db.Column(db.Integer, default = 0)
    #errmsg = db.Column(db.String(500))

    def __init__(self, **kwargs):
        self.title = kwargs['title']
        self.sendto = kwargs['sendto']
        self.remote_addr = kwargs['remote_addr']
        self.from_app = kwargs['from_app']
        #self.errmsg = kwargs['errmsg']
