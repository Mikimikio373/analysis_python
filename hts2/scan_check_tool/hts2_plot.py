import os
import sys
import json
import yaml
import hts2_plot_module as myplt

basepath = 'A:/Test/not_test/0009'

# sensor_exposureをたたいているコマンドから、scan_chech_toolの場所を特定
pythonpath = os.path.split(sys.argv[0])[0]
# sensorの場所情報を書いてあるフォルダを読み込み
with open(os.path.join(pythonpath, 'sensor_pos.yml'), 'rb') as f:
    y_load = yaml.safe_load(f)
y_sorted = sorted(y_load, key=lambda x: x['pos'])

ScanAreaParam = os.path.join(basepath, 'ScanAreaParam.json')
with open(ScanAreaParam, 'rb') as sap:
    sap_json = json.load(sap)

with open(os.path.join(basepath, 'ValidViewHistory.json'), 'rb') as f:
    vvh_json = json.load(f)

myplt.not_all(basepath, y_sorted, sap_json, vvh_json, 30000)

