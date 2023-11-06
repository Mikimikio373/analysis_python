import json
import numpy as np
import matplotlib.pyplot as plt

vvh_path = 'A:/Test/20231016unit4-88_1/ValidViewHistory.json'

with open(vvh_path, 'rb') as f:
    vvh = json.load(f)

x = np.arange(24)
# print(vvh[0]['Nogs'][3])
for i in range(len(vvh)):
    if vvh[i]['ScanLines']['Layer'] == 1:
        plt.plot(x, vvh[i]['Nogs'][3], 'x-')

plt.show()
