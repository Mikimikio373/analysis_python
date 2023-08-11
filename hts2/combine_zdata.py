import csv
import sys
import pandas as pn
import numpy as np
import os

basepath = 'Q:/minami/20230809_ali-z'
zlist = [[], []]
for m in range(2):
    for s in range(5, 9):
        csv_path = os.path.join(basepath, 'Module{}'.format(m), 'sensor-{}'.format(s), 'peak_z.csv')
        if not os.path.exists(csv_path):
            print('there is no file: {}'.format(csv_path))
            zlist[m].append(0)
            continue
        csv_data = pn.read_csv(csv_path, header=None, dtype=float)
        print(csv_data[0].values)
        zlist[m].append(np.mean(csv_data[0].values))

print(zlist)
df = pn.DataFrame()
df['module0'] = zlist[0]
df['module1'] = zlist[1]
write_csv = os.path.join(basepath, 'zlist.csv')
df.to_csv(write_csv, index=False)