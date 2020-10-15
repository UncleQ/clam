#import tushare as ts
import pandas as pd
from dateutil.parser import parse
import datetime
import requests


def get_num(days):
    if days <= 29.5:
        return 1
    days = days - 30
    if 0 <= days < 29.5:
        return 1
    elif 29.5 <= days < 41.8:
        return 2
    elif 41.8 <= days < 51.1:
        return 3
    elif 51.1<= days <= 66:
        return 5
    elif 66 < days < 83.5:
        return 8
    elif 83.5 <= days < 106.5:
        return 13
    elif 106.5 <= days < 135.3:
        return 21
    elif 135.3 <= days < 172.2:
        return 34
    elif 172.2 <= days <= 219:
        return 55
    elif 219 < days < 278.6:
        return 89
    elif 278.6 <= days < 354.4:
        return 144
    elif 354.4 <= days < 450.8:
        return 233
    elif 450.8 <= days < 573.4:
        return 377
    elif 573.4 <= days < 729.4:
        return 610
    elif 729.4 <= days < 927.7:
        return 987
    elif 927.7 <= days < 1180.1:
        return 1597
    elif 1180.1 <= days < 1501.1:
        return 2584
    elif 1501.1 <= days < 1909.5:
        return 4181
    elif 1909.5 <= days < 2428.9:
        return 6765
    elif 2428.9 <= days < 3089.6:
        return 10946
    elif 3089.6 <= days <= 3930:
        return 17711
    elif 3930 < days < 4999.1:
        return 28657
    elif 4999.1 <= days < 6358.9:
        return 46368
    elif 6358.9 <= days < 8088.6:
        return 75025
    elif 8088.6 <= days < 10288.9:
        return 121393
    elif 10288.9 <= days < 13087.7:
        return 196418
    elif 13087.7 <= days < 16647.8:
        return 317811
    elif 16647.8 <= days < 21176.3:
        return 514229
    elif 21176.3 <= days < 26936.7:
        return 832040
    elif 26936.7 <= days <= 34264:
        return 1346269
    elif 34264 < days < 43584.5:
        return 2178309
    elif 43584.5 <= days < 55440.3:
        return 3524578
    elif 55440.3 <= days < 70521.2:
        return 5702887
    elif 70521.2 <= days < 89704.3:
        return 9227465
    else:
        return 0


def get_last_date():
    with open('label_data.csv', 'r') as fp:
        lines = fp.readlines()
        last_line = lines[-1]
        tmp_list = last_line.split(',')
        return tmp_list[0], tmp_list[1] 


def add_line_to_file(line):
    with open('label_data.csv', encoding='utf-8',mode='a') as file:  
        file.write(line)  


def get_new_line(cur_date):
    delta = datetime.timedelta(days=1)
    d = parse(cur_date)
    yesterday_date = (d - delta).strftime('%Y%02m%02d')
    url = 'http://quotes.money.163.com/service/chddata.html?code=0000001&start=%s&end=%s&fields=TCLOSE;HIGH;LOW;TOPEN;LCLOSE;CHG;PCHG;VOTURNOVER;VATURNOVER' % (cur_date, cur_date)
    print(url)
    r = requests.get(url) 
    data = r.content.decode('gbk')
    print(data)
    print(type(data))
    l = data.split('\r\n')
    values = l[1].split(',')
    print(values)
    values[0] = values[0].replace('-', '/')
    values[11] = str(float(values[11]))
    del values[7]
    del values[1]
    del values[1]
    return values
    

def main():
    start_day = parse('1993/2/16')
    last_index, last_date = get_last_date() 
    cur_date = datetime.date.today().strftime('%Y/%m/%d')
    if cur_date == last_date:
        return
    print('add %s data' % cur_date)
    cur_date = datetime.date.today().strftime('%Y%02m%02d')
    tmp_date = datetime.date.today()
    print(type(tmp_date))
    #cur_date = '20200819'
    values = get_new_line(cur_date)
    cur_index = int(last_index)
    cur_index = cur_index + 1
    values.insert(0, str(cur_index))
    cur_day = parse(cur_date)
    diff_day = cur_day - start_day
    num = get_num(float(diff_day.days))
    values.append(str(num))
    line = ','.join(values)
    print(line)
    add_line_to_file(line + '\n')
    return
    

if __name__ == '__main__':
    main()

