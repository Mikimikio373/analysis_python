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
press_f_name = 'all_diff_press_20230412in20230412cut_one/dff_press_edit20230412.csv'
press_path = os.path.join(basepath, 'pressure_chech', 'plot_and_data', press_f_name)
tilt_f_name = 'all_tilt_from20230403_to20230412with_line/edit_data.csv'
tilt_path = os.path.join(basepath, 'keishakei', tilt_f_name)
output_name = 'tilt_edit.csv'
output_path = os.path.join(basepath, 'keishakei', output_name)

if not os.path.exists(press_path):
    sys.exit('there is no \"ondotori\" file: {}'.format(press_path))
if not os.path.exists(tilt_path):
    sys.exit('there is no \"tilt\" file: {}'.format(tilt_path))

press_pn = pn.read_csv(press_path)
print(press_pn)
press_unix_time = []
print('press data size: {}'.format(len(press_pn)))
for i in range(len(press_pn)):
    v_time_t = datetime.datetime.strptime(press_pn['v recorder time'][i], '%Y-%m-%d %H:%M:%S')
    atm_time_t = datetime.datetime.strptime(press_pn['atm ondotori time'][i], '%Y-%m-%d %H:%M:%S')
    press_unix_time.append(v_time_t.timestamp())

tilt_pn = pn.read_csv(tilt_path)
tilt_time_unix = []

print('tilt data size : {}'.format(len(tilt_pn)))
for i in range(len(tilt_pn)):
    time_t = datetime.datetime.strptime(tilt_pn['Date/Time'][i], '%Y-%m-%d %H:%M:%S')
    tilt_time_unix.append(time_t.timestamp())


cut_press_time = []
cut_dffpress = []
cut_atmpress = []
cut_temp_tent = []
cut_temp_shell = []
cut_tilt_ax1 = []
cut_tilt_ax2 = []
cut_tilt_ax3 = []
cut_tilt_ay1 = []
cut_tilt_ay2 = []
cut_tilt_ay3 = []
cut_tilt_time = []
print(len(press_unix_time))
for i in range(len(press_unix_time)):
    if i % 100 == 0:
        print('\r{}/{} ended'.format(i, len(press_pn)), end='')
    tilt_time_index = getNearestIndex(tilt_time_unix, press_unix_time[i])
    time_dist = press_unix_time[i] - tilt_time_unix[tilt_time_index]
    if abs(time_dist) > 10:
        continue
    cut_press_time.append(press_unix_time[i])
    cut_dffpress.append(press_pn['raw diff pressure'][i])
    cut_atmpress.append(press_pn['atm pressure'][i])
    cut_temp_tent.append(press_pn['outside temperature'][i])
    cut_temp_shell.append(press_pn['shell temperature'][i])
    cut_tilt_ax1.append(tilt_pn['ax1'][tilt_time_index])
    cut_tilt_ax2.append(tilt_pn['ax2'][tilt_time_index])
    cut_tilt_ax3.append(tilt_pn['ax3'][tilt_time_index])
    cut_tilt_ay1.append(tilt_pn['ay1'][tilt_time_index])
    cut_tilt_ay2.append(tilt_pn['ay2'][tilt_time_index])
    cut_tilt_ay3.append(tilt_pn['ay3'][tilt_time_index])
    cut_tilt_time.append(tilt_time_unix[tilt_time_index])
print('\n{}/{} ended'.format(len(press_pn), len(press_pn)))

edit_pn = pn.DataFrame()
edit_pn['recorder time'] = cut_press_time
edit_pn['dff pressure'] = cut_dffpress
edit_pn['atm pressure'] = cut_atmpress
edit_pn['outside temperature'] = cut_temp_tent
edit_pn['shell temperature'] = cut_temp_shell
edit_pn['tilt time'] = cut_tilt_time
edit_pn['ax1'] = cut_tilt_ax1
edit_pn['ax2'] = cut_tilt_ax2
edit_pn['ax3'] = cut_tilt_ax3
edit_pn['ay1'] = cut_tilt_ay1
edit_pn['ay2'] = cut_tilt_ay2
edit_pn['ay3'] = cut_tilt_ay3
edit_pn.to_csv(output_path, index=False)
