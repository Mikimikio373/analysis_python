import json
import os

path = 'A:/Xdrive_copy/AdminParam/HTS2/Offset/General/OffsetParam.json'

with open(path, 'rb') as f:
    param = json.load(f)

for i in range(len(param['Array'])):
    param['Array'][i]['Z'] = 0

out_path = os.path.join(os.path.dirname(path), 'OffsetParam_non.json')
with open(out_path, 'w') as f:
    json.dump(param, f, indent=2)