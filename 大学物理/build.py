from email.utils import encode_rfc2231
from fileinput import filename
import os
import shutil

path = os.getcwd()
objname = path[path.rfind('\\') + 1:]
myfile =  open(f'{path}/_sidebar.md', 'w')

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

for dirpath, dirnames, files in os.walk('.', topdown=False):
    if not (dirpath.endswith('章')):
        continue
    print(f'* {dirpath[2:]}')
    myfile.write(f'* {dirpath[2:]}\n')
    for file_name in files:
        if(file_name.endswith('.md')):
            print(f'  * [{file_name[:-3]}]({objname}/{dirpath[2:]}/{file_name})')
            myfile.write(f'  * [{file_name[:-3]}]({objname}/{dirpath[2:]}/{file_name})\n')

myfile.close()