import json
import os
import sys
from matplotlib import pyplot as plt
import numpy as np

basepath = 'Q:/minami/20230810_ali-z/Module1/sensor-7'

thick = []
for i in range(1, 51):
    json_path = os.path.join(basepath, 'pich0.5um-{}'.format(i), 'IMAGE00_AREA-1', 'V00000000_L0_VX0000_VY0000_0_064.json')
    with open(json_path, 'r') as f:
        j = json.load(f)
    tmp = float(j['Images'][0]['z']) - float(j['Images'][-1]['z'])
    tmp *= 1000
    thick.append(tmp)

plt.hist(thick)
plt.show()
np.savetxt(os.path.join(basepath, 'thickness.csv'), np.asarray(thick), delimiter=',')