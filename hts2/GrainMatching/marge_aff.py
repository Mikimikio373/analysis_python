import os.path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

basepath = 'Q:/minami/202300912_aff'
bairitu = []
kaiten = []
id = np.arange(24)

for i in range(2):
    for j in range(12):
        tar_dir = os.path.join(basepath, 'Module{}'.format(i), 'sensor-{}'.format(j), 'affdata_surf.csv')
        df = pd.read_csv(tar_dir)
        bai = (abs(df['a'][0]) + abs(df['d'][0]))/2
        kai = (abs(df['b'][0]) / bai + abs(df['c'][0]) / bai) / 2
        bairitu.append(bai*1000)
        kaiten.append(bai)

plt.plot(id, bairitu, 'x')
plt.xticks(np.arange(24))
plt.xlabel('sensor ID')
plt.ylabel('倍率 [um/pixel]', fontname='MS Gothic')
plt.grid()
plt.show()

