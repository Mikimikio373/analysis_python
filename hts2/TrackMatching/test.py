import json
import os.path

basepath = 'A:/Test/check_FASER/m222-pl002_30cm-2'
ori_beta = os.path.join(basepath, 'Beta_EachImagerParam.json')
new_aff = os.path.join(basepath, 'Affine_param_new_origin3.json')
out_beta = os.path.join(basepath, 'Beta_EachImagerParam_new.json')

with open(ori_beta, 'rb') as f:
    j_ori_beta = json.load(f)
with open(new_aff, 'rb') as f:
    j_new_aff = json.load(f)


for i in range(24):
    for j in range(6):
        if j == 1:
            continue
        j_ori_beta[i]['Aff_coef'][j] = j_new_aff[i]['Aff_coef'][j]

with open(out_beta, 'w') as f:
    json.dump(j_ori_beta, f, indent=2)
