import os
import shutil
import glob
import sys

path = 'Q:/minami/20230910_nog2'
if os.path.exists(path):
    print('This file already exists:{}.\nDo you want to overwrite? y/n'.format(path))
    answer = input()
    if not answer == 'y':
        sys.exit('interrupt the program')

os.makedirs(path, exist_ok=True)
ori_path = 'A:/Test'

if not len(sys.argv) == 2:
    sys.exit('please input number of files')
file_num = int(sys.argv[1])

os.chdir(path)
currend_dir = os.getcwd()
print('current directry: {}'.format(currend_dir))

for i in range(file_num):
    tar_dir = '{}'.format(i)
    if os.path.exists(tar_dir):
        shutil.rmtree(tar_dir)

    param_path = os.path.join(ori_path, '{:04}'.format(i), 'PARAMS')
    shutil.copytree(param_path, os.path.join(tar_dir, 'PARAMS'))
    for p in glob.glob(os.path.join(ori_path, '{:04}'.format(i), '*.json'), recursive=True):
        if os.path.isfile(p):
            shutil.copy2(p, tar_dir)

