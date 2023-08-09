import os
import subprocess
import sys
import pandas as pn
import numpy as np
from matplotlib import pyplot as plt

for j in range(5, 9):
    basepath = 'Q:/minami/20230809_ali-z/Module1/sensor-{}'.format(j)
    if not os.path.exists(basepath):
        continue

    i_max = 4
    for i in range(1, i_max):
        tar_dir = os.path.join(basepath, 'pich0.5um-{}'.format(i))
        command_z = 'python C:\\Users\\flab\\analysis_python\\hts2\\z_search.py {}'.format(tar_dir)
        subprocess.run(command_z, shell=True)

    nogmax_z = []
    for i in range(1, i_max):
        tar_dir = os.path.join(basepath, 'pich0.5um-{}'.format(i))
        csv_path = os.path.join(tar_dir, 'nog.csv')
        data = pn.read_csv(csv_path)
        nogmax_index = np.argmax(data['nog'])
        nogmax_z.append(float(data['z'][nogmax_index]))

    np.savetxt(os.path.join(basepath, 'peak_z.csv'), np.asarray(nogmax_z), delimiter=',')
    # print(np.max(nogmax_z), np.min(nogmax_z), np.max(nogmax_z) - np.min(nogmax_z))