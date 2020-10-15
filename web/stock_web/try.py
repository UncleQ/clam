import subprocess
import shutil

shutil.copy('/opt/1.txt', '/opt/2.txt')
a = [1,'a']
print(type(a))
p = subprocess.Popen('tail -100 /opt/work/stock/nohup.out',shell=True,stdout=subprocess.PIPE)
out,err = p.communicate()
#for line in out.splitlines():
    #print(str(line, encoding = "utf-8"))
