import json
import math
import numpy as np

import pandas as pd
import os
import shutil

ori_dir = 'Q:/minami/202300912_aff'
marge_dir = 'Q:/minami/deadpixel'
# for module in range(2):
#     for sensor in range(12):
#         ori_csv = os.path.join(ori_dir, 'Module{}'.format(module), 'sensor-{}'.format(sensor), 'deadpixel_list.csv')
#         shutil.copy2(ori_csv, os.path.join(marge_dir, '{}-{:02}_pixel-list.csv'.format(module, sensor)))

ori_json = os.path.join(marge_dir, 'DeadPixel.json')
with open(ori_json) as f:
    ori_jsondata = json.load(f)

for i in range(24):
    module = math.floor(i / 12)
    sensor = i % 12
    df = pd.read_csv(os.path.join(marge_dir, '{}-{:02}_pixel-list.csv'.format(module, sensor)))
    deadpixel_list = []
    for j in range(len(df)):
        pair = [float(df['px'][j]), float(df['py'][j])]
        deadpixel_list.append(pair)
    print(deadpixel_list)
    ori_jsondata[i]["DeadPixel"] = deadpixel_list

print(ori_jsondata[0])
out_json = os.path.join(marge_dir, 'DeadPixel_One_Third.json')
with open(out_json, 'w') as f:
    json.dump(ori_jsondata, f, indent=2)

