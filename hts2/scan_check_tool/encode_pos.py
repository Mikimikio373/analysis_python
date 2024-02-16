import json

import matplotlib.pyplot as plt

vvh_path = 'P:/GRAINE_B23-01/20240110_bug/ValidViewHistory.json'

with open(vvh_path, 'rb') as f:
    vvh = json.load(f)

print(list(vvh[0]['Positions0']))
x = [[], []]
y = [[], []]

for i in range(len(vvh)):
    x[0].append(vvh[i]['Positions0']['X'])
    x[1].append(vvh[i]['Positions1']['X'])
    y[0].append(vvh[i]['Positions0']['Y'])
    y[1].append(vvh[i]['Positions1']['Y'])

plt.scatter(x[0], y[0], marker='o', c='None', edgecolors='r', label='Position0')
plt.scatter(x[1], y[1], marker='s', c='None', edgecolors='b', label='Position1')
plt.legend()
plt.xlabel('Stage X [mm]')
plt.ylabel('Stage Y [mm]')
plt.show()

