import os
import sys

import numpy as np
from matplotlib import pyplot as plt
import pandas as pn

basepath = 'Q:/minami/20230810_ali-z/Module1/sensor-7'


for i in range(1, 51):
    csv_path = os.path.join(basepath, 'pich0.5um-{}'.format(i), 'nog.csv')
    df = pn.read_csv(csv_path)
    zlist = np.asarray(df['z'].values)
    zlis_1 = (zlist + 12.105596) * 1000
    plt.plot(zlis_1, df['nog'].values, '-x')
    # plt.show()
    # sys.exit()

plt.xlabel('z [um]')
plt.ylabel('nog')
plt.grid()
# plt.show()
out_path = os.path.join(basepath, 'nog_combine.png')
plt.savefig(out_path, dpi=300)