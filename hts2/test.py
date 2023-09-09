import os
import shutil
import glob

path = 'Q:/minami/20230909_nog'
ori_path = 'A:/Test'

os.chdir(path)
currend_dir = os.getcwd()
print('current directry: {}'.format(currend_dir))

for i in range(21):
    tar_dir = '{}'.format(i)
    if os.path.exists(tar_dir):
        shutil.rmtree(tar_dir)

    param_path = os.path.join(ori_path, '{:04}'.format(i), 'PARAMS')
    shutil.copytree(param_path, os.path.join(tar_dir, 'PARAMS'))
    for p in glob.glob(os.path.join(ori_path, '{:04}'.format(i), '*.json'), recursive=True):
        if os.path.isfile(p):
            shutil.copy2(p, tar_dir)


