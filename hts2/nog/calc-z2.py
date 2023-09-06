import os
import subprocess
import sys
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt

py_dir = os.getcwd()

if len(sys.argv) != 2:
    exit('command line error. please \"basepath\"')

basepath = sys.argv[1]
if not os.path.exists(basepath):
    exit('there is no directory: {}'.format(basepath))

i_max = 101
startskip = 2
endskip = 4

#rename
os.chdir(basepath)
current_dir = os.getcwd()
print('directory changed, current path: {}'.format(current_dir))
for a in range(1, i_max):
    tar_file_name = '1_{:02}'.format(a)
    if not os.path.exists(tar_file_name):
        continue

    # print(tar_file_name, a + 1)
    os.rename(tar_file_name, '{}'.format(a + 1))

os.chdir(py_dir)
current_dir = os.getcwd()
print('directory changed, current path: {}'.format(current_dir))
#fit piezo
for i in range(1, i_max):
    tar_dir = os.path.join(basepath, '{}'.format(i))
    if not os.path.exists(tar_dir):
        print('skipped: {}'.format(tar_dir))
        continue
    command_fit = 'python C:\\Users\\flab\\analysis_python\\hts2\\nog\\fit_piezo-z.py {} {} {}'.format(tar_dir, startskip, endskip)
    subprocess.run(command_fit, shell=True)

#z-search
for i in range(1, i_max):
    tar_dir = os.path.join(basepath, '{}'.format(i))
    if not os.path.exists(tar_dir):
        print('skipped: {}'.format(tar_dir))
        continue
    command_z = 'python C:\\Users\\flab\\analysis_python\\hts2\\nog\\z-search2.py {} {} {}'.format(tar_dir, startskip, endskip)
    subprocess.run(command_z, shell=True)

nogmax_z = []
for i in range(1, i_max):
    tar_dir = os.path.join(basepath, '{}'.format(i))
    csv_path = os.path.join(tar_dir, 'nog.csv')
    if not os.path.exists(csv_path):
        print('skipped: {}'.format(csv_path))
        continue
    data = pd.read_csv(csv_path)
    nogmax_index = np.argmax(data['nog'])
    nogmax_z.append(float(data['z'][nogmax_index]))

np.savetxt(os.path.join(basepath, 'peak_z.csv'), np.asarray(nogmax_z), delimiter=',')
print(np.max(nogmax_z), np.min(nogmax_z), np.mean(nogmax_z), (np.max(nogmax_z) - np.min(nogmax_z))*1000)