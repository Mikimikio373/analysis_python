import json
import os
import matplotlib.pyplot as plt
import pandas as pd
import yaml

basepath = 'R:\\minami\\20230531_aff\\Module1\\sensor-7'
out_path = os.path.join(basepath, 'check_StartPoint', 'encode.csv')

yaml_path = os.path.join(basepath, 'AreaScan4Param.yml')
with open(yaml_path, 'rb') as yml:
    param = yaml.safe_load(yml)

x_size = param['Area'][0]['NViewX']  # x方向の大きさ
y_size = param["Area"][0]["NViewY"]  # y方向の大きさ
layer = param["Area"][0]["NLayer"]
npicture = param["NPictures"]
plate_sum = layer * x_size * y_size

view = 0
sx_0 = 0
sy_0 = 0
sx = []
sy = []
dsx = []
dsy = []
line = []
for i in range(y_size + 1):
    if i < 2:
        view += x_size * i
    else:
        view += x_size + 1
    oripath = os.path.join(basepath, 'IMAGE00_AREA-1', 'V{:08}_L{}_VX{:04}_VY{:04}_0_{:03}.json'.format(view, 0, 0, 0, npicture))
    json_open = open(oripath)
    j = json.load(json_open)
    if i == 0:
        sx_0 = j['Images'][0]['x']
        sy_0 = j['Images'][0]['y']
        dx = 0
        dy = 0
    else:
        dx = j['Images'][0]['x'] - sx_0
        dy = j['Images'][0]['y'] - sy_0
    line.append(i)
    sx.append(j['Images'][0]['x'])
    sy.append(j['Images'][0]['y'])
    dsx.append(dx)
    dsy.append(dy)

out = pd.DataFrame()
out['time'] = line
out['sx'] = sx
out['sy'] = sy
out['dsx'] = dsx
out['dsy'] = dsy

out.to_csv(out_path, index=False)