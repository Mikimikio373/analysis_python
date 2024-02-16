import json
import os.path
from math import sin, cos
import numpy as np

tar_dir = 'A:/Test/check_FASER/m222-pl002_30cm-1'

ori_path = os.path.join(tar_dir, 'Beta_EachImagerParam.json')
with open(ori_path, 'rb') as f:
    param = json.load(f)

theta = 0.00003
rot = np.array([[cos(theta), -sin(theta)], [sin(theta), cos(theta)]])
print(rot)

for i in range(len(param)):
    aff_coef = param[i]['Aff_coef']
    array = np.array([[aff_coef[0], aff_coef[1]], [aff_coef[2], aff_coef[3]]])
    array = rot @ array
    param[i]['Aff_coef'][0] =array[0][0]
    param[i]['Aff_coef'][1] = array[0][1]
    param[i]['Aff_coef'][2] = array[1][0]
    param[i]['Aff_coef'][3] = array[1][1]


out_path = os.path.join(tar_dir, 'Beta_EachImagerParam_rot.json')
with open(out_path, 'w') as f:
    json.dump(param, f, indent=2)