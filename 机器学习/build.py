#!/usr/bin/python3
from email.utils import encode_rfc2231
from fileinput import filename
import string
import numpy as np
import os
import platform

path = os.getcwd()
if(platform.system() == 'Windows'):
    objname = path[path.rfind('\\') + 1:]
else:
    objname = path[path.rfind('/') + 1:]
myfile =  open(f'{path}/_sidebar.md', 'w')
dict = { "一" : 1, "二" : 2, "三" : 3, "四" : 4, "五" : 5, "六" : 6, "七" : 7, "八" : 8, "九" : 9, "十" : 10,
         "十一" : 11, "十二" : 12, "十三" : 13, "十四" : 14, "十五" : 15, "十六" : 16}

with os.scandir(path) as entries:
    flag = 0
    for entry in entries:
        _file_name = entry.name
        if _file_name.endswith('.md') and not _file_name.startswith('_'):
            if flag == 0:
                myfile.write("* 其它\n")
                flag = 1
            myfile.write(f'  * [{_file_name[:-3]}]({objname}/{_file_name})\n')
            print(f'  * [{_file_name[:-3]}]({objname}/{_file_name})\n')

filelist = [[0] * 101 for x in range(20)]
chaplist = [0] * 20
for dirpath, dirnames, files in os.walk('.', topdown=False):
    if(dirpath == '.'): continue
    print(f'* {dirpath[2:]}')
    myfile.write(f'* {dirpath[2:]}\n')
    #chaplist[dict[dirpath[-2:-1]]] = dirpath[-2:-1]
    #index = 0
    for file_name in files:
        if(file_name.endswith('.md') and not (file_name.startswith('_')) or file_name.startswith('/R')):
            print(f'  * [{file_name[:-3]}]({objname}/{dirpath[2:]}/{file_name})')
            myfile.write(f'  * [{file_name[:-3]}]({objname}/{dirpath[2:]}/{file_name})\n')
            #filelist[dict[dirpath[-2:-1]]][index] = f'  * [{file_name[:-3]}]({objname}/{dirpath[2:]}/{file_name})\n'
            #index += 1

'''
Chaplist = [x for x in chaplist if x != 0]
for x in Chaplist:
    myfile.write(f'* 第{x}章\n')
    for name in filelist[dict[x]]:
        if name != 0:
            myfile.write(name)
'''

myfile.close()