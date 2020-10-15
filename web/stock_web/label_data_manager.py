import os
from dateutil.parser import parse
import datetime

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


def get_date_num(new_date):
    start_day = parse('1993/2/16')
    new_day = parse(new_date)
    diff_day = new_day - start_day
    return get_num(float(diff_day.days))


def get_last_date():
    with open('/opt/work/stock/label_data_web.csv', 'r') as fp:
        lines = fp.readlines()
        last_line = lines[-1]
        tmp_list = last_line.split(',')
        return tmp_list[0], tmp_list[1] 


def add_line_to_file(line):
    with open('/opt/work/stock/label_data_web.csv', encoding='utf-8',mode='a') as file:  
        file.write(line)  


def add_new_line(new_line_info): 
    last_index, last_date = get_last_date()
    last_index = int(last_index)
    if last_date == new_line_info['date']:
        pass    
    else:
        tmp_list = list()
        tmp_list.append(str(last_index+1))
        tmp_list.append(new_line_info['date'].replace('-', '/'))
        tmp_list.append(new_line_info['end'])
        tmp_list.append(new_line_info['high'])
        tmp_list.append(new_line_info['low'])
        tmp_list.append('0')
        tmp_list.append('0')
        tmp_list.append('0')
        tmp_list.append(new_line_info['volume'])
        tmp_list.append(new_line_info['amount'])
        tmp_list.append(str(get_date_num(new_line_info['date'])))
        new_line = ','.join(tmp_list)
        add_line_to_file(new_line + '\n')
    

def main():
    pass

if __name__ == '__main__':
    main()
