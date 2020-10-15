import psutil
import time
import os
import subprocess


def get_last_completed_image():
    pic_dir = '/opt/work/stock/pic_8p'
    pic_list = list()
    for root, dirs, files in os.walk(pic_dir):    
        for f in files:
            if f.endswith('-release-8P.png'):
                full_path = os.path.join(root, f)
                pic_list.append(f)
    return pic_list[-1]


def get_last_completed_mission():
    pic_dir = '/opt/work/stock/pic_8p'
    pic_list = list()
    for root, dirs, files in os.walk(pic_dir):    
        for f in files:
            if f.endswith('-release-8P.png'):
                full_path = os.path.join(root, f)
                pic_list.append(f)
    last_mission = pic_list[-1]
    pos = last_mission.find('-')
    last_mission = last_mission[:pos]
    pos = last_mission.find('_')
    last_mission = last_mission[pos + 1:]
    pos = last_mission.find('_')
    last_mission = last_mission[pos + 1:]
    return last_mission


def get_cur_sub_process():
    pids = psutil.pids()
    sub_process = None
    for i in range(2):
        for item in pids:
            try:
                p = psutil.Process(item)
                cmdline = p.cmdline() 
                if 'train71.py' in cmdline or 'predict106.py' in cmdline:
                    if cmdline[0] == 'python':
                        return p
            except (psutil.ZombieProcess, psutil.AccessDenied, psutil.NoSuchProcess):
                continue
        time.sleep(1)
    return None


def stop_cur_mission():
    sub_process = get_cur_sub_process()
    while sub_process is not None:
        cmdline = sub_process.cmdline()
        if cmdline[1] == 'train71.py':
            sub_process.kill()    
        if cmdline[1] == 'predict106.py':
            sub_process.kill()    
            return
        time.sleep(1)
        sub_process = get_cur_sub_process()
    p = subprocess.Popen('rm -f /opt/work/stock/nohup.out',shell=True,stdout=subprocess.PIPE)


def get_train_pos():
    result = ''
    p = subprocess.Popen('tail -100 /opt/work/stock/nohup.out',shell=True,stdout=subprocess.PIPE)
    out,err = p.communicate()
    for line in out.splitlines():
        str_line = str(line, encoding = "utf-8")
        if str_line.startswith('Epoch'):
            result = str_line[str_line.find(' ') + 1:]
    return result


def start_mission(mission_date):
    cmd = 'sh /opt/work/stock/start_mission.sh %s' % mission_date
    p = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE)
    out,err = p.communicate()
    for line in out.splitlines():
        str_line = str(line, encoding = "utf-8")
    time.sleep(5)
    if has_running_mission() is not None:
        return True
    else:
        return False 

def has_running_mission():
    pids = psutil.pids()
    for item in pids:
        p = psutil.Process(item)
        cmdline = p.cmdline() 
        if len(cmdline) < 2:
            continue
        if 'train71.py' == cmdline[1] and cmdline[0] == 'python':
            process_pos = get_train_pos()
            return 'train71', cmdline[3], cmdline[9], process_pos
        if 'predict106.py' == cmdline[1] and cmdline[0] == 'python':
            return 'predict106.py', cmdline[9]
    return None

def main():
    get_last_completed_mission()
    return
    result = has_running_mission()
    if result != None:
        print(result[0])
        print(result[1])
    else:
        print('has no running mission')

if __name__ == '__main__':
    main()

