import json
import math

import pandas as pd
import shutil
import os
import numpy as np

affparam_path = 'Q:/minami/affine_param/AffineParam.json'
with open(affparam_path) as f:
    affparam = json.load(f)

# print(affparam)

marge_base = 'Q:/minami/affine_param'
aff_base = 'Q:/minami/202300912_aff'
pq_base = 'Q:/minami/20230914_Ali2/calc_ali'

# for i in range(2):
#     for j in range(12):
#         aff_path = os.path.join(aff_base, 'Module{}'.format(i), 'sensor-{}'.format(j), 'affdata_surf.csv')
#         shutil.copy2(aff_path, os.path.join(marge_base, '{}-{:02}_aff.csv'.format(i, j)))
#         pq_path = os.path.join(pq_base, 'vs{}-{:02}_fit.csv'.format(i, j))
#         shutil.copy2(pq_path, os.path.join(marge_base, '{}-{:02}_pq.csv'.format(i, j)))

for i in range(24):
    module = math.floor(i / 12)
    sensor = i % 12
    aff = os.path.join(marge_base, '{}-{:02}_aff.csv'.format(module, sensor))
    aff_df = pd.read_csv(aff)
    pq = os.path.join(marge_base, '{}-{:02}_pq.csv'.format(module, sensor))
    pq_df = pd.read_csv(pq)
    coef = [aff_df['a'][0], aff_df['b'][0], aff_df['c'][0], aff_df['d'][0], -pq_df['dx'][0], -pq_df['dy'][0]]
    print(coef)
    affparam[i]["Aff_coef"] = coef

dump = os.path.join(marge_base, 'aff_one_third.json')
with open(dump, 'w') as f:
    json.dump(affparam, f, indent=2)