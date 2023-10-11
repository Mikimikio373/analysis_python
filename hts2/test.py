import json

path = 'A:/Test/unit19-8_maxarea/Beta_EachShotParam.json'

with open(path, 'rb') as f:
    param = json.load(f)

print(len(param))
