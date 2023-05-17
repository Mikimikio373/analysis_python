import pandas as pn
import numpy as np
import sys
import os
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime
from matplotlib.backends.backend_pdf import PdfPages


def getNearestIndex(input_list, num):
    # リスト要素と対象値の差分を計算し最小値のインデックスを取得
    idx = np.abs(np.asarray(input_list) - num).argmin()
    return idx


def getNearestValue(input_list, num):
    idx = np.abs(np.asarray(input_list) - num).argmin()
    return list[idx]


csvpath = '//Users//minamihideyuki//data//lab//for_Australia//pressure_chech'
vol_name = 'all_diff_press_20230328.csv'
atm_ondotori_name = 'all_atm_ondotori.csv'
temp_ondotori_name = 'all_temp_ondotori.csv'
out_dir = os.path.join(csvpath, 'plot_and_data')
if not os.path.exists(out_dir):
    os.makedirs(out_dir)

vol_path = os.path.join(csvpath, vol_name)
atm_ondotori_path = os.path.join(csvpath, atm_ondotori_name)
temp_ondotori_path = os.path.join(csvpath, temp_ondotori_name)

dt_now = datetime.datetime.now()
dt_now_str = dt_now.strftime('%Y%m%d')
out_vol = os.path.join(out_dir, vol_path[:-4] + '_edit_' + dt_now_str + '.csv')
out_atm_ondotori = os.path.join(out_dir, atm_ondotori_name[:-4] + '_edit_' + dt_now_str + '.csv')
out_temp_ondotori = os.path.join(out_dir, temp_ondotori_name[:-4] + '_edit_' + dt_now_str + '.csv')
output_filepath = os.path.join(out_dir, 'dff_press_edit' + dt_now_str + '.csv')
output_pdf = os.path.join(out_dir, 'dff_press_plot' + dt_now_str + '.pdf')

# V to P 一次変換式の傾き(a)と切片(b)
a = 497.74
b = -1492.3
if not os.path.exists(vol_path):
    sys.exit('there is no \"voltage\" file :{}'.format(vol_path))
if not os.path.exists(atm_ondotori_path):
    sys.exit('there is no \"atm_ondotori\" file :{}'.format(atm_ondotori_path))

# V to P 計算
####################
vol_pn = pn.read_csv(vol_path)
vol_pn = vol_pn.drop(vol_pn.index[0:2])
vol_pn = vol_pn.drop(columns=['Date/Time.1', 'No.2', 'No.3', 'No.4'])
vol_pn = vol_pn[vol_pn['No.1'].astype('float') > 3.1]
vol_pn = vol_pn.reset_index(drop=True)

pressure = []
press_time = []
press_time_unix = []
for i in range(0, len(vol_pn)):
    p_tmp = a * float(vol_pn['No.1'][i]) + b
    pressure.append(p_tmp)
    press_time.append(datetime.datetime.strptime(vol_pn['Date/Time'][i], '%Y-%m-%d %H:%M:%S'))
    press_time_unix.append(datetime.datetime.strptime(vol_pn['Date/Time'][i], '%Y-%m-%d %H:%M:%S').timestamp())

max_point = np.argmax(pressure)  # 圧力が最初に最大になる時の配列番号を取得
vol_pn = vol_pn.drop(columns='Date/Time')
vol_pn['time'] = press_time
vol_pn['pressure'] = pressure
# vol_pn = vol_pn.drop(range(max_point + 144))  # 圧力が安定するまでの時間(最大値ポイントから１時間後)のデータを削除
vol_pn = vol_pn.reset_index(drop=True)

# 大気圧取得用温度取り
#########################
f_atm_ondotori = open(atm_ondotori_path, 'r', encoding='shift_jis')
f_atm_ondotori_line = f_atm_ondotori.readlines()
atm_ondotori_time = []
atm_ondotori_time_unix = []
temprature = []
at_press = []
for i in range(4, len(f_atm_ondotori_line) - 1):  # ４行分飛ばして、最終行はデータがない可能性が高いので読まない
    split_line = f_atm_ondotori_line[i].split('\"')
    # time_t = datetime.datetime.strptime(split_line[1], '%Y/%m/%d %H:%M\'%S')
    time_t = datetime.datetime.strptime(split_line[1], '%Y/%m/%d %H:%M\'%S') + datetime.timedelta(minutes=30)
    atm_ondotori_time.append(time_t)
    atm_ondotori_time_unix.append(time_t.timestamp())
    temprature.append(float(split_line[5]))
    at_press.append(float(split_line[9]))

# 整形してファイル出力
atm_ondotori_pn = pn.DataFrame()
atm_ondotori_pn['time'] = atm_ondotori_time
atm_ondotori_pn['temperature'] = temprature
atm_ondotori_pn['pressure'] = at_press
atm_ondotori_pn.to_csv(out_atm_ondotori, index=False)

##シェル内温度用おんどとり
temp_ondotori_pn = pn.read_csv(temp_ondotori_path)
temp_ondotori_pn = temp_ondotori_pn.drop(columns=['Group Name', 'Device Name'])
temp_ondotori_pn = temp_ondotori_pn[3:]
temp_ondotori_pn = temp_ondotori_pn.reset_index(drop=True)
temp_ondotori_time = []
temp_ondotori_time_unix = []
for i in range(len(temp_ondotori_pn)):
    # time_t = datetime.datetime.strptime(temp_ondotori_pn['Model'][i], '%Y/%m/%d %H:%M:%S')
    time_t = datetime.datetime.strptime(temp_ondotori_pn['Model'][i], '%Y/%m/%d %H:%M:%S') + datetime.timedelta(minutes=30)
    temp_ondotori_time.append(time_t)
    temp_ondotori_time_unix.append(time_t.timestamp())

temp_ondotori_pn['time'] = temp_ondotori_time
temp_ondotori_pn = temp_ondotori_pn.drop(columns=['Model'])
temp_ondotori_pn = temp_ondotori_pn.rename(columns={'Serial': 'temperature'})
temp_ondotori_pn = temp_ondotori_pn.reindex(columns=['time', 'temperature'])
temp_ondotori_pn['temperature'] = temp_ondotori_pn['temperature'].astype('float')
temp_ondotori_pn.to_csv(out_temp_ondotori, index=False)

##
##温度補正&output pandas作成
##

##時刻合わせ
print('pressure first time: {}'.format(vol_pn['time'][0]))
print('atm ondotori first time: {}'.format(atm_ondotori_pn['time'][0]))
print('temp ondotori first time: {}'.format(temp_ondotori_pn['time'][0]))

minimum_list_size = min(len(vol_pn), len(atm_ondotori_pn), len(temp_ondotori_pn))
list_mode = 0  # 1がvoltege, 2がatm ondotori, 3がtemp ondotori
if len(vol_pn) == minimum_list_size:
    print('minimum list size is \"volo_pn\"')
    list_mode = 1
elif len(atm_ondotori_pn) == minimum_list_size:
    print('minimum list size is \"atm_ondotori_pn\"')
    list_mode = 2
else:
    print('minimum list size is \"temp_ondotori_pn\"')
    list_mode = 3

output_time_v = []
output_v = []
output_raw_diff_press = []
output_fixed_dff_press = []
output_time_atm_ondotori = []
output_temp_outside = []
output_atm = []
output_time_temp_ondotori = []
output_temp_shell = []

same_time_point = 0
vol_num = 0
atm_first_point = 0
temp_first_point = 0

print(len(vol_pn), len(press_time_unix))

for i in range(minimum_list_size):
    time_vol_unix = press_time_unix[i]
    time_atm_index = getNearestIndex(atm_ondotori_time_unix, time_vol_unix)
    time_temp_index = getNearestIndex(temp_ondotori_time_unix, time_vol_unix)
    if i == 0:
        atm_first_point = time_atm_index
        temp_first_point = time_temp_index
    time_diff_atm = atm_ondotori_pn['time'][time_atm_index] - vol_pn['time'][i]
    time_diff_temp = temp_ondotori_pn['time'][time_temp_index] - vol_pn['time'][i]
    if abs(time_diff_atm.total_seconds()) > 150.0 or abs(time_diff_temp.total_seconds()) > 150.0:
        continue
    # 温度補正
    fix_press = (vol_pn['pressure'][i] + atm_ondotori_pn['pressure'][time_atm_index]) * (
                temp_ondotori_pn['temperature'][temp_first_point] + 273.16) / (
                            temp_ondotori_pn['temperature'][time_temp_index] + 273.16) - atm_ondotori_pn['pressure'][
                    atm_first_point]
    # 友亮補正
    # fix_press = vol_pn['pressure'][i] + (1 - (temp_ondotori_pn['temperature'][temp_first_point] + 273.16) / (
    #             temp_ondotori_pn['temperature'][time_temp_index] + 273.16)) * vol_pn['pressure'][0]
    output_time_v.append(vol_pn['time'][i])
    output_v.append(vol_pn['No.1'][i])
    output_raw_diff_press.append(vol_pn['pressure'][i])
    output_fixed_dff_press.append(fix_press)
    output_time_atm_ondotori.append(atm_ondotori_pn['time'][time_atm_index])
    output_temp_outside.append(atm_ondotori_pn['temperature'][time_atm_index])
    output_atm.append(atm_ondotori_pn['pressure'][time_atm_index])
    output_time_temp_ondotori.append(temp_ondotori_pn['time'][time_temp_index])
    output_temp_shell.append(temp_ondotori_pn['temperature'][time_temp_index])

# 整形後ファイル出力
output_pn = pn.DataFrame()
output_pn['v recorder time'] = output_time_v
output_pn['voltage'] = output_v
output_pn['raw diff pressure'] = output_raw_diff_press
output_pn['fixed dff pressure'] = output_fixed_dff_press
output_pn['atm ondotori time'] = output_time_atm_ondotori
output_pn['outside temperature'] = output_temp_outside
output_pn['atm pressure'] = output_atm
output_pn['temp ondotori time'] = output_time_temp_ondotori
output_pn['shell temperature'] = output_temp_shell
output_pn.to_csv(output_filepath, index=False)

##
# time : Pressur plot
##



out_pdf = PdfPages(output_pdf)
Minute_fmt = mdates.DateFormatter("%m-%d\n%H:%M")
locator = mdates.DayLocator()
## raw and fix pressure
fig = plt.figure(tight_layout=True)
ax = fig.add_subplot(111)
ax.plot(output_pn['v recorder time'], output_pn['raw diff pressure'], 'x', label='raw data', ms=1)
ax.plot(output_pn['v recorder time'], output_pn['fixed dff pressure'], 'x', label='fixed pressure', ms=1)
ax.xaxis.set_major_formatter(Minute_fmt)
ax.xaxis.set_major_locator(locator)
ax.legend(loc='upper left')
ax.grid()
ax.set_ylim(100, 1000)
ax.set_yscale('log', base=10)
ax.tick_params(axis='x', labelsize=5)
ax.set_ylabel('pressure [hPa]')
out_pdf.savefig()
# plt.savefig(os.path.join(csvpath, 'test1.png'), dpi=300)
fig.clf()

## raw and fixed pressure, and atm pressure
ax_diff = fig.add_subplot(111)
ax_diff.plot(output_pn['v recorder time'], output_pn['raw diff pressure'], 'x', label='raw data', ms=1)
ax_diff.plot(output_pn['v recorder time'], output_pn['fixed dff pressure'], 'x', label='fixed pressure', ms=1)
ax_diff.set_xlim([output_pn['v recorder time'][0], output_pn.iloc[-1]['v recorder time']])
ax_diff.xaxis.set_major_formatter(Minute_fmt)
ax_diff.xaxis.set_major_locator(locator)
ax_diff.tick_params(axis='x', labelsize=5)
ax_diff.set_ylabel('pressure [hPa]')
h1, l1 = ax_diff.get_legend_handles_labels()
ax_diff.grid()
ax_diff.set_ylim(100, 1000)
ax_diff.set_yscale('log', base=10)

ax_atm = ax.twinx()
ax_atm.plot(atm_ondotori_pn['time'], atm_ondotori_pn['pressure'], 'x', label='atmosphere', c='r', ms=1, alpha=0.5)
ax_atm.set_xlim([output_pn['v recorder time'][0], output_pn.iloc[-1]['v recorder time']])
ax_atm.xaxis.set_major_formatter(Minute_fmt)
ax_atm.xaxis.set_major_locator(locator)
ax_atm.set_ylim(900, 980)
ax_atm.set_yscale('log', base=10)
ax_atm.set_ylabel('pressure [hPa]')
h2, l2 = ax_atm.get_legend_handles_labels()

ax_diff.legend(h1 + h2, l1 + l2, loc='upper left')
out_pdf.savefig()
fig.clf()

## raw and fixed pressure, and temperature
ax_diff = fig.add_subplot(111)
ax_diff.plot(output_pn['v recorder time'], output_pn['raw diff pressure'], 'x', label='raw data', ms=1)
ax_diff.plot(output_pn['v recorder time'], output_pn['fixed dff pressure'], 'x', label='fixed pressure', ms=1)
ax_diff.set_xlim([output_pn['v recorder time'][0], output_pn.iloc[-1]['v recorder time']])
ax_diff.xaxis.set_major_formatter(Minute_fmt)
ax_diff.xaxis.set_major_locator(locator)
ax_diff.tick_params(axis='x', labelsize=5)
ax_diff.set_ylabel('pressure [hPa]')
h1, l1 = ax_diff.get_legend_handles_labels()
ax_diff.grid()
ax_diff.set_ylim(100, 1000)
ax_diff.set_yscale('log', base=10)

ax_temp = ax.twinx()
ax_temp.plot(temp_ondotori_pn['time'], temp_ondotori_pn['temperature'], 'x', label='temprerature', c='b', ms=1, alpha=0.5)
ax_temp.set_xlim([output_pn['v recorder time'][0], output_pn.iloc[-1]['v recorder time']])
ax_temp.xaxis.set_major_formatter(Minute_fmt)
ax_temp.xaxis.set_major_locator(locator)
ax_temp.set_ylabel('temperature [°C]')
h2, l2 = ax_temp.get_legend_handles_labels()

ax_diff.legend(h1 + h2, l1 + l2, loc='upper left')
out_pdf.savefig()
fig.clf()

ax_atm = fig.add_subplot(111)
ax_atm.plot(atm_ondotori_pn['time'], atm_ondotori_pn['pressure'], 'x', label='atmosphere', c='r', ms=1, alpha=0.5)
ax_atm.xaxis.set_major_formatter(Minute_fmt)
ax_atm.xaxis.set_major_locator(locator)
ax_atm.set_ylim(900, 980)
# ax_atm.set_xlim([output_pn['v recorder time'][0], output_pn.iloc[-1]['v recorder time']])
ax_atm.set_yscale('log', base=10)
ax_atm.grid()
ax_atm.tick_params(axis='x', labelsize=5)
ax_diff.set_ylabel('pressure [hPa]')
out_pdf.savefig()
fig.clf()

ax_temp = fig.add_subplot(111)
ax_temp.plot(temp_ondotori_pn['time'], temp_ondotori_pn['temperature'], 'x', label='temprerature', c='b', ms=1, alpha=0.5)
# ax_temp.set_xlim([output_pn['v recorder time'][0], output_pn.iloc[-1]['v recorder time']])
ax_temp.xaxis.set_major_formatter(Minute_fmt)
ax_temp.xaxis.set_major_locator(locator)
ax_temp.grid()
ax_temp.tick_params(axis='x', labelsize=5)
ax_temp.set_ylabel('temperature [°C]')
out_pdf.savefig()
fig.clf()

out_pdf.close()
