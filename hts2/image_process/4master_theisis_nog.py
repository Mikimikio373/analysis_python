import json

import numpy as np
import matplotlib.pyplot as plt
# from matplotlib import rc
# rc('text', usetex=True)

jsonpath = 'B:/data/powerpoint/HTS2_data/4master_theisis/plot_nog/VVH_unit4-pl088.json'

with open(jsonpath, 'rb') as f:
    vvh = json.load(f)

view = 2000
imager = 18
print(vvh[view]['ScanLines']['Layer'])
nogs = vvh[view]['Nogs'][imager]
x = np.arange(1, len(nogs) + 1)
# print(x)
# print(nogs)

plt.figure(tight_layout=True)
plt.plot(x, nogs, 'o')
plt.xticks(range(0, len(nogs) + 1, 2), fontsize=12)
plt.yticks(fontsize=12)
plt.xlabel('Image number' + r'$\simeq$' + 'Z', fontsize=18)
plt.ylabel('Number of Grains (NOG)', fontsize=18)
outpath = 'B:/data/powerpoint/HTS2_data/4master_theisis/plot_nog/nog-v{}_i{}.png'.format(view, imager)
plt.savefig(outpath, dpi=300)
# plt.show()

