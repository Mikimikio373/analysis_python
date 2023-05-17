import os
import sys
import matplotlib.pyplot as plt
import pandas as pn
import datetime
import numpy as np

def getNearestIndex(input_list, num):
    # リスト要素と対象値の差分を計算し最小値のインデックスを取得
    idx = np.abs(np.asarray(input_list) - num).argmin()
    return idx


def getNearestValue(input_list, num):
    idx = np.abs(np.asarray(input_list) - num).argmin()
    return input_list[idx]

basepath = '/Users/minamihideyuki/data/lab/for_Australia'
ondotori_f_name = '20230403_outpress.csv'
ondotori_path = os.path.join(basepath, 'pressure_chech', 'logging_data', 'atm_ondotori', ondotori_f_name)
tilt_f_name = '20230403_tilt_edit.csv'
tilt_path = os.path.join(basepath, 'keishakei', tilt_f_name)
output_name = 'test_ax1.csv'
output_path = os.path.join(basepath, 'keishakei', output_name)

if not os.path.exists(ondotori_path):
    sys.exit('there is no \"ondotori\" file: {}'.format(ondotori_path))
if not os.path.exists(tilt_path):
    sys.exit('there is no \"tilt\" file: {}'.format(tilt_path))



f_atm_ondotori = open(ondotori_path, 'r', encoding='shift_jis')
f_atm_ondotori_line = f_atm_ondotori.readlines()
atm_ondotori_time = []
atm_ondotori_time_unix = []
temprature = []
at_press = []
atm_first_time = datetime.datetime.now()
atm_elapsed_time = []
for i in range(4, len(f_atm_ondotori_line) - 1):  # ４行分飛ばして、最終行はデータがない可能性が高いので読まない
    split_line = f_atm_ondotori_line[i].split('\"')
    # time_t = datetime.datetime.strptime(split_line[1], '%Y/%m/%d %H:%M\'%S')
    time_t = datetime.datetime.strptime(split_line[1], '%Y/%m/%d %H:%M\'%S') + datetime.timedelta(minutes=30)
    if i == 4:
        atm_first_time = time_t
    atm_ondotori_time.append(time_t)
    atm_ondotori_time_unix.append(time_t.timestamp())
    atm_elapsed_time.append(((time_t - atm_first_time).total_seconds()) / 3600)
    temprature.append(float(split_line[5]))
    at_press.append(float(split_line[9]))

tilt_pn = pn.read_csv(tilt_path)

tilt_time_unix = []
for i in range(len(tilt_pn)):
    time_t = datetime.datetime.strptime(tilt_pn['Date/Time'][i], '%Y-%m-%d %H:%M:%S')
    tilt_time_unix.append(time_t.timestamp())


cut_temp = []
cut_ondotori_time = []
cut_tilt_ax1 = []
cut_tilt_ax2 = []
cut_tilt_ax3 = []
cut_tilt_ay1 = []
cut_tilt_ay2 = []
cut_tilt_ay3 = []
cut_tilt_time = []
print(len(atm_ondotori_time_unix))
for i in range(len(atm_ondotori_time_unix)):
    tilt_time_index = getNearestIndex(tilt_time_unix, atm_ondotori_time_unix[i])
    time_dist = atm_ondotori_time_unix[i] - tilt_time_unix[tilt_time_index]
    if abs(time_dist) > 10:
        continue
    cut_temp.append(temprature[i])
    cut_tilt_ax1.append(tilt_pn['ax1'][tilt_time_index])
    cut_tilt_ax2.append(tilt_pn['ax2'][tilt_time_index])
    cut_tilt_ax3.append(tilt_pn['ax3'][tilt_time_index])
    cut_tilt_ay1.append(tilt_pn['ay1'][tilt_time_index])
    cut_tilt_ay2.append(tilt_pn['ay2'][tilt_time_index])
    cut_tilt_ay3.append(tilt_pn['ay3'][tilt_time_index])
    cut_ondotori_time.append(atm_ondotori_time[i])
    cut_tilt_time.append(tilt_pn['Date/Time'][tilt_time_index])

edit_pn = pn.DataFrame()
edit_pn['ondotori time'] = cut_ondotori_time
edit_pn['temperature'] = cut_temp
edit_pn['tilt time'] = cut_tilt_time
edit_pn['ax1'] = cut_tilt_ax1
edit_pn['ax2'] = cut_tilt_ax2
edit_pn['ax3'] = cut_tilt_ax3
edit_pn['ay1'] = cut_tilt_ay1
edit_pn['ay2'] = cut_tilt_ay2
edit_pn['ay3'] = cut_tilt_ay3
edit_pn.to_csv(output_path, index=False)
