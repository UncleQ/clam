#!/usr/bin/bash
python train71.py -n 5 -t $1 -e $2 -d $3 -o /opt/work/stock/result
python train71.py -n 10 -t $1 -e $2 -d $3 -o /opt/work/stock/result
python train71.py -n 19 -t $1 -e $2 -d $3 -o /opt/work/stock/result
python train71.py -n 40 -t $1 -e $2 -d $3 -o /opt/work/stock/result
python train71.py -n 60 -t $1 -e $2 -d $3 -o /opt/work/stock/result
python train71.py -n 90 -t $1 -e $2 -d $3 -o /opt/work/stock/result
python train71.py -n 120 -t $1 -e $2 -d $3 -o /opt/work/stock/result
python train71.py -n 240 -t $1 -e $2 -d $3 -o /opt/work/stock/result
python predict106.py -m /opt/work/stock/result -e $2 -t $1 -d $3
