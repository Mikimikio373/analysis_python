import json
import math
import os.path

import pandas as pd

ori_aff_path = 'X:/Project_v3/AdminParam/HTS2/AffineParam.json'
tar_dir = 'A:/Test/TrackMatch/trackmatching4aff-m222-pl001/TrackMatching4Aff'   # 行列成分のみ計算したaff_paramのpath
out_json = 'A:/Test/TrackMatch/Affine_param_abcd.json'
imager_num = 24
with open(ori_aff_path, 'rb') as f:
    aff = json.load(f)

for i in range(imager_num):
    module = math.floor(i / 12)
    sensor = i % 12
    tar_csv = os.path.join(tar_dir, '{:02}_{:02}'.format(module, sensor), 'aff.csv')
    aff_data = pd.read_csv(tar_csv)
    aff[i]['Aff_coef'][0] = aff_data['a'][0]
    aff[i]['Aff_coef'][1] = aff_data['b'][0]
    aff[i]['Aff_coef'][2] = aff_data['c'][0]
    aff[i]['Aff_coef'][3] = aff_data['d'][0]
    aff[i]['Aff_coef'][4] = 0
    aff[i]['Aff_coef'][5] = 0

with open(out_json, 'w') as f:
    json.dump(aff, f, indent=2)

