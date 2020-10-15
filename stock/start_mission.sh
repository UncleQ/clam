#!/usr/bin/bash
echo $1
cd /opt/work/stock
rm -f nohup.out
#sh bakjob.sh
#python3 update_label_data.py
nohup sh do106.sh 100 500 $1 >/dev/null 2>&1 &
