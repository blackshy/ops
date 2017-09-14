import requests
from flask import current_app, request, render_template, make_response
from flask_restful import Api, Resource, reqparse
from threading import Thread 
from . import zbx
from .. import db
from .forms import DateRangeForm
import time
import json
import textwrap
import logging
import datetime
import requests
from collections import defaultdict
from decorator import debug, async
from zabbix_api import ZBXAPI
from operator import itemgetter

import sys
reload(sys)
sys.setdefaultencoding("utf-8")

app = current_app._get_current_object()
api = Api(zbx)

@api.resource('/')
class Zabbix(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('start_time', type = str, location = ['form', 'headers', 'values', 'json'])
        self.reqparse.add_argument('end_time',   type = str, location = ['form', 'headers', 'values', 'json'])
        self.reqparse.add_argument('hosts',      type = str, location = ['form', 'headers', 'values', 'json'])
        self.args = self.reqparse.parse_args()
        self.remote_addr = request.remote_addr
        self.zbx = ZBXAPI(
                url = app.config['ZBX_URL'],
                username = app.config['ZBX_USER'],
                password = app.config['ZBX_PASS']
                )
        
        self.itemid_with_host = []
        self.vms_info = []
        self.stimestr = None
        self.etimestr = None
        self.stimestamp = 0
        self.etimestamp = 0
        self.hosts = []

#        self.host_ip = [ 
#                '10.0.8.247',
#                '10.0.8.248',
#                '10.0.8.249',
#                '10.0.8.250',
#                '10.0.8.251',
#                '10.0.8.252',
#                '10.0.9.251',
#                '10.0.9.252'
#                ]

    def get(self):
        form = DateRangeForm()
        result = render_template('zabbix/top.html', form = form)
        return make_response(result)

    def post(self):
        return self.index()

    def index(self):
        args = self.args
        form = DateRangeForm()
        self.stimestr = args['start_time']
        self.etimestr = args['end_time']
        self.stimestamp = self.get_start_time(self.stimestr)
        self.etimestamp = self.get_end_time(self.etimestr)
        self.hosts = args['hosts'].split(',')
        ips = []
        _vms = self.get_vms_on_host(self.hosts)
        for vms in _vms:
            for vm in vms:
                ips.append(vm['ip'])
                self.vms_info.append(vm)

        hids = self.zbx.get_hostid_by_ip(ips = ips)
        hostids = [ host['hostid'] for host in hids ]

        #keyword = 'system.cpu.util[,user]'
        keyword = 'system.cpu.load[percpu,avg1]'
        items = self.zbx.get_item_id_by_keyword(hostids = hostids, keyword = keyword)

        hostid_with_itemid = { item['hostid']: item['itemid'] for item in items }
        hostids = [ item['hostid'] for item in items ]
        hostid_with_host = self.zbx.get_hosts_by_id(hostids)

        itemid_with_host = {}
        for hostid in hostid_with_itemid.keys():
            itemid = hostid_with_itemid[hostid]
            host = hostid_with_host[hostid]
            itemid_with_host[itemid] = host
        self.itemid_with_host = itemid_with_host

        itemids = [ i['itemid'] for i in items ]

        trend = self.zbx.get_trend(itemids = itemids, stime = self.stimestamp, etime = self.etimestamp)
        result = self.get_top_ten(trend)
        #result = json.dumps(a, sort_keys=True, indent=4)
        result = render_template('zabbix/top_ten.html', result = result, form = form)
        return make_response(result)

    #@async
#    def get_trend(self, itemids=None, rrange=0):
#        result = self.zbx.get_trend(itemids, rrange)
#        return result
        
    def get_top_ten(self, data = None):
        data_by_day = self.flush_by_day(data)
        result = {}
        items = data_by_day['data']
        #for day, items in data_by_day.items():
            #rows_by_avg = sorted(items, key=itemgetter('avg', 'max'), reverse=True)
        rows_by_avg = sorted(items, key=itemgetter('avg', 'max'))
        #data_by_day['data'] = rows_by_avg[0:50]
        data_by_day['data'] = rows_by_avg
        return data_by_day

    def flush_by_day(self, data = None):
        in_day = {}
        day = data
        #for day in data:
        #print day
        #today = time.strftime('%Y-%m-%d', time.localtime(float(day[0]['clock'])))
        ## gather each server's data by itemid
        all_servers_in_day = defaultdict(list)
        for hour in day:
            all_servers_in_day[hour['itemid']].append(hour)

        ## sort each server' data by max, avg, min
        time_list = []
        max_list = []
        avg_list = []
        min_list = []
        one_day_all_servers = []
        for itemid in all_servers_in_day:
            each_server_final = {}
            for each_server_per_hour in all_servers_in_day[itemid]:
                max_list.append(float(each_server_per_hour['value_max']))
                #min_list.append(float(each_server_per_hour['value_min']))
                avg_list.append(float(each_server_per_hour['value_avg']))
            each_server_final['max'] = max(max_list)
            #each_server_final['min'] = min(min_list)
            each_server_final['avg'] = 0
            if len(avg_list):
                each_server_final['avg'] = sum(avg_list) / len(avg_list)
            #server_host = self.zbx.get_hosts_by_id(itemid)
            each_server_final['server'] = self.itemid_with_host[itemid]
            #server_info = self.get_server_description(self.itemid_with_host[itemid])
            for vm in self.vms_info:
                if vm['ip'] == self.itemid_with_host[itemid]:
                    server_info = vm
                    break
            each_server_final['desc'] = server_info['description']
            each_server_final['host'] = server_info['fatherip']
            one_day_all_servers.append(each_server_final)
        in_day['stime'] = self.stimestr
        in_day['etime'] = self.etimestr
        in_day['data'] = one_day_all_servers
        return in_day

    def get_start_time(self, strdate):
        #timestamp = int(time.mktime(datetime.datetime.combine(datetime.date.today(), datetime.time.min).timetuple())) - (86400 * sday)
        timestamp = time.mktime(datetime.datetime.strptime(strdate, "%Y-%m-%d").timetuple())
        return int(timestamp)

    def get_end_time(self, strdate):
        #timestamp = int(time.mktime(datetime.datetime.combine(datetime.date.today(), datetime.time.max).timetuple())) - (86400 * eday)
        timestamp = time.mktime(datetime.datetime.strptime(strdate, "%Y-%m-%d").timetuple())
        return int(timestamp) + 86400

    def get_server_description(self, ip):
        #print ip
        r = requests.get(app.config['SERVER_DETAIL_API_URL'] + ip)
        return r.json()

    def get_vms_on_host(self, ip):
        ip_url_format = ''
        for i in ip:
            ip_url_format += '&ip[]=' + i
        print app.config['GET_VMS_API_URL'] + ip_url_format.lstrip('&')
        r = requests.get(app.config['GET_VMS_API_URL'] + ip_url_format.lstrip('&'))
        return r.json()
