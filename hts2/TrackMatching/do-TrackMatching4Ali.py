import math
import os
import subprocess

import yaml
basepath = 'A:/Test/TrackMatch/trackmatching4ali-m222-pl002'
exe_path = 'C:/Users/flab/source/repos/myproject/x64/Release/TrackMatching4Ali.exe'
# sensorの配置情報が書いてあるymlファイルの読み込み
with open('sensor_pos.yml', 'rb') as f:
    y_load = yaml.safe_load(f)

origin_imager = 12
mode = 2
angcut = 0.05
phcut = 10
volcut = 20
rough_cut = 0.1
output_rage = 0.0015

os.chdir(basepath)
currend_dir = os.getcwd()
print('path changed. current path: {}'.format(currend_dir))

for target_imager in range(24):
    pos = y_load[target_imager]['pos']
    tarX = 1.178708 * (pos % 8)
    tarY = 0.572948 * math.floor(pos / 8)
    print(tarX, tarY)
    cmd = '{} {} {} {} {} {} {} {} {} {} {}'.format(exe_path, origin_imager, target_imager, mode, angcut, phcut, volcut, tarX, tarY, rough_cut, output_rage)
    subprocess.run(cmd, shell=True)

