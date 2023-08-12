import os
import subprocess
import sys
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt

basepath = 'Q:/minami/20230811_dip/1-7/0.5um'

i_max = 51
for i in range(1, i_max):
    tar_dir = os.path.join(basepath, '{}'.format(i))
    command_z = 'python C:\\Users\\flab\\analysis_python\\hts2\\nog\\z-search2.py {}'.format(tar_dir)
    subprocess.run(command_z, shell=True)

nogmax_z = []
for i in range(1, i_max):
    tar_dir = os.path.join(basepath, '{}'.format(i))
    csv_path = os.path.join(tar_dir, 'nog.csv')
    data = pd.read_csv(csv_path)
    nogmax_index = np.argmax(data['nog'])
    nogmax_z.append(float(data['z'][nogmax_index]))

np.savetxt(os.path.join(basepath, 'peak_z.csv'), np.asarray(nogmax_z), delimiter=',')
print(np.max(nogmax_z), np.min(nogmax_z), np.mean(nogmax_z), (np.max(nogmax_z) - np.min(nogmax_z))*1000)