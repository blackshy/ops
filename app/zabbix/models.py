from .. import db
from datetime import datetime, timedelta

class AssetsDB(db.Model):
    __tablename__ = 'assets'
    id = db.Column(db.Integer, primary_key = True)
    hostname = db.Column(db.String(255))
    add_time = db.Column(db.DateTime, default = datetime.now())
    update_time = db.Column(db.DateTime, default = datetime.now())

    def __init__(self, **kwargs):
        self.hostname = kwargs['hostname']
        self.add_time = kwargs['add_time']
        self.update_time = kwargs['update_time']

#class ISPLocation(db.Model):
#    __tablename__ = 'isp_location'
#    id = db.Column(db.Integer, primary_key = True)
#
#class CarbinetLocation(db.Model):
#    __tablename__ = 'carbinet_location'
#    id = db.Column(db.Integer, primary_key = True)
#
#class ServerLocation(db.Model):
#    __tablename__ = 'server_location'
#    id = db.Column(db.Inter, primary_key = True)
