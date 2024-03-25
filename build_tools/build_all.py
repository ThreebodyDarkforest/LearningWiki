import os
import os.path as osp
import json
import argparse

PATH = osp.dirname(osp.dirname(osp.abspath(__file__)))
IGNORE = ['.configs', '.gitlab', '.metion', '.git', '.obsidian', 'assets', 'build_tools']

def chinese_num_to_arabic(chinese_num):
    """
    将中文数字转换为阿拉伯数字。
    """
    chinese_arabic_map = {
        "一": 1, "二": 2, "三": 3, "四": 4,
        "五": 5, "六": 6, "七": 7, "八": 8,
        "九": 9, "十": 10, "十一": 11, "十二": 12,
        "十三": 13, "十四": 14, "十五": 15, "十六": 16
    }
    return chinese_arabic_map.get(chinese_num, 0)

def sort_directories(dirnames):
    """
    根据目录名中的中文数字对目录进行排序。
    """
    dirnames.sort(key=lambda x: chinese_num_to_arabic(x[1:-1].split("章")[0]))

def process_single(root, topic):
    file_path = osp.join(root, topic)
    readme = osp.join(file_path, 'README.md')
    if not osp.exists(readme):
        with open(readme, 'w') as f:
            f.write('## ' + topic)
    file = osp.join(file_path, '_sidebar.md')
    myfile = open(file, 'w')

    # 遍历指定路径，写入文件头部
    with os.scandir(file_path) as entries:
        flag = 0
        for entry in entries:
            _file_name = entry.name
            if _file_name.endswith('.md') and not _file_name.startswith('_'):
                if flag == 0:
                    myfile.write("* 其它\n")
                    flag = 1
                myfile.write(f'  * [{_file_name[:-3]}]({topic}/{_file_name})\n')
                print(f'  * [{_file_name[:-3]}]({topic}/{_file_name})\n')

    dirnames = [d for d in os.listdir(file_path) if osp.isdir(osp.join(file_path, d))]
    sort_directories(dirnames)  # 对目录进行排序

    # 遍历目录和子目录，写入Markdown文件链接
    for dirname in dirnames:
        dirroot = osp.join(file_path, dirname)
        print(f'* {dirname}')
        myfile.write(f'* {dirname}\n')
        for file_name in os.listdir(dirroot):
            if file_name.endswith('.md') and not (file_name.startswith('_')) or file_name.startswith('/R'):
                print(f'  * [{file_name[:-3]}]({topic}/{dirname}/{file_name})')
                myfile.write(f'  * [{file_name[:-3]}]({topic}/{dirname}/{file_name})\n')

    myfile.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--root', default=PATH, help='root of learning wiki')
    
    args = parser.parse_args()

    content = ''
    for dir in os.listdir(args.root):
        if osp.isdir(dir) and dir not in IGNORE:
            process_single(args.root, dir)
            
            file = f'{dir}/README.md'
            content += f'* [{dir}]({file})\n'

    with open(osp.join(args.root, '_sidebar.md'), 'w') as f:
        f.write(content)