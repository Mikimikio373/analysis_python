import json

import matplotlib.pyplot as plt
import numpy as np
ori = 'A:/Test/TrackMatch/AffineParam_20230925.json'
new = 'A:/Test/TrackMatch/Affine_param_abcd.json'

with open(ori, 'rb') as f:
    ori_aff = json.load(f)
with open(new, 'rb') as f:
    new_aff = json.load(f)

a = [[], []]
d = [[], []]
imager_num = 24

for i in range(24):
    a[0].append(abs(ori_aff[i]['Aff_coef'][0]))
    a[1].append(abs(new_aff[i]['Aff_coef'][0]))
    d[0].append(abs(ori_aff[i]['Aff_coef'][3]))
    d[1].append(abs(new_aff[i]['Aff_coef'][3]))
a_max = np.max(a)
d_max = np.max(d)
print(a_max)
x = range(imager_num)
plt.plot(x, np.asarray(a[0]) / a_max, 'x', label='current data')
plt.plot(x, np.asarray(a[1]) / a_max, 'x', label='new data')
plt.xticks(x)
plt.ylim(0.997, 1)
plt.legend()
plt.grid()
plt.savefig('A:/Test/TrackMatch/compare_a.png', dpi=300)
plt.clf()

plt.plot(x, np.asarray(d[0]) / d_max, 'x', label='current data')
plt.plot(x, np.asarray(d[1]) / d_max, 'x', label='new data')
plt.xticks(x)
plt.ylim(0.997, 1)
plt.legend()
plt.grid()
plt.savefig('A:/Test/TrackMatch/compare_d.png', dpi=300)
