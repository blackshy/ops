import requests
import time
import json
import textwrap
import logging
import datetime
from pyzabbix import ZabbixAPI

import sys
reload(sys)
sys.setdefaultencoding("utf-8")

class ZBXAPI(object):

    def __init__(self,
                 url = "http://localhost/zabbix/api_jsonrpc.php",
                 username = "admin",
                 password = "zabbix"
                 ):
        self.url = url
        self.username = username
        self.password = password
        self.zapi = ZabbixAPI(self.url)
        self.zapi.login(self.username, self.password)
        self.zapi.session.verify = False
        self.zapi.timeout = 5

    def get_version(self):
        return self.zapi.api_version()

    ''' Section for host ( by id or ip) actions
    '''
    def get_hosts_by_id(self, hostids = None):
        hosts = self.zapi.host.get(hostids = hostids)
        hostid_with_host = { host['hostid']: host['host'] for host in hosts }
        result = hostid_with_host
        return result

    def get_hostid_by_ip(self, ips):
        hosts = []
        for ip in ips:
            s = time.time()
            host = self.zapi.hostinterface.get(output="extend", filter={"ip": ip})
            print ip
            if host:
                hosts.append(host[0])
                print host
            e = time.time()
            print e-s
        return hosts

    def get_item_id_by_keyword(self, hostids, keyword):
        result = self.zapi.item.get(hostids = hostids, search={"key_": keyword})
        return result

    def get_history(self, itemids, rrange = 0):
        time_start = int(time.mktime(datetime.datetime.combine(datetime.date.today(), datetime.time.min).timetuple())) - (86400 * rrange)
        time_end = int(time.mktime(datetime.datetime.combine(datetime.date.today(), datetime.time.max).timetuple())) - (86400 * rrange)
        result = self.zapi.history.get(time_from=time_start, time_till=time_end, history=0, sortfield='clock', sortorder='DESC',itemids=itemids)
        return result

    def get_trend_in_one_day(self, itemids, rrange = 0):
        time_start = int(time.mktime(datetime.datetime.combine(datetime.date.today(), datetime.time.min).timetuple())) - (86400 * rrange)
        time_end = int(time.mktime(datetime.datetime.combine(datetime.date.today(), datetime.time.max).timetuple())) - (86400 * rrange)
        result = self.zapi.trend.get(time_from=time_start, time_till=time_end, output="extend", itemids=itemids)
        return result

    def get_trend(self, itemids, stime, etime):
        if not etime:
            etime = int(time.mktime(datetime.datetime.combine(datetime.date.today(), datetime.time.max).timetuple()))
        result = self.zapi.trend.get(time_from=stime, time_till=etime, output=['itemid', 'value_avg', 'value_max'], itemids=itemids)
        return result
