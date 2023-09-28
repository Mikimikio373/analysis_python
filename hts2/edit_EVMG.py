import json
import os

basepath = 'Q:/minami/EVMG'

ori_json = os.path.join(basepath, 'default.json')

with open(ori_json, 'rb') as f:
    ori_j = json.load(f)

for i in range(len(ori_j['ImagerControllerParamList'])):
    # print(ori_j['ImagerControllerParamList'][i]['TargetBrightness'])
    ori_j['ImagerControllerParamList'][i]['TargetBrightness'] = 220

out_json = os.path.join(basepath, 'hts2_default.json')
with open(out_json, 'w') as f:
    json.dump(ori_j, f, indent=2)