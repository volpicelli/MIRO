#!/bin/bash
cd "$(dirname "$0")"

systemctl stop miro
pkill miro
systemctl daemon-reload
systemctl start miro
systemctl restart nginx
#
#source ./env/bin/activate
#now=$(date)
#wd_log="wd_$(date +'%Y_%m_%d').log"
#kill -9 $(ps aux | grep wd | grep -v grep | awk '{print $2}' | tr '\n'  ' ') > /dev/null 2>&1;
#python wd.py > logs/$wd_log &
