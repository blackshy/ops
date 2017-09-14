#!/bin/bash

###SCRIPT_NAME:weixin.sh###
###send message from weixin for zabbix monitor###
###wuhf###
###V1-2015-08-25###

User="$1"
Title="$2"
Message="$3"

#/usr/bin/curl -XPOST "http://10.0.8.45:5000/weixin/" -F "message=${Message}" -F "title=${Title}" -F "sendto=${User}" -F "app=zabbix"
/usr/bin/curl -XPOST "http://127.0.0.1:5000/weixin/" -F "message=${Message}" -F "title=${Title}" -F "sendto=user" -F "app=zabbix"
