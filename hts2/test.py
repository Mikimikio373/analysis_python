import json
import math

ori_path = 'A:/Test/20231026_for_beta_ali/Beta_EachShotParam_org.json'
path = 'A:/Test/20231026_for_beta_ali/Beta_EachShotParam.json'

with open(path, 'rb') as f:
    sjson = json.load(f)
with open(ori_path, 'rb') as f:
    sjson_ori = json.load(f)

for i in range(0, len(sjson), 24):
    print(sjson[i]['View'], sjson_ori[i]['View'])

# for i in range(1764):
#     print(math.floor(i / 84) * 28 + (i % 28))
