##標準ライブラリ
import csv
import os
import sys
import datetime
import time
import subprocess
import shutil

##非標準ライブラリ
import numpy as np
from scipy.optimize import curve_fit
import pandas as pn
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.backends.backend_pdf import PdfPages

# global変数を用意
click_count = 0  # クリックした回数
xvline_list = []  # クリックした場所の、xポジションを記録
cmap = plt.get_cmap('tab20')
cut_mode = 2 #0何もなし 1:指定時刻でカット 2:上限下限指定
cut_time = datetime.datetime(2023, 3, 24, hour=14, minute=44, second=12) #再加圧後
cut_time2 = datetime.datetime(2023, 4, 21, hour=10, minute=0, second=0) #リハ前再加圧
vol_name = 'all_diff_press_20230430.csv'
atm_ondotori_name = 'all_atm_ondotori20230430.csv'
temp_ondotori_name = 'all_temp_ondotori20230430.csv'

point_select_mode = 1 #0:クリックで選択、1:リストで選択
# specific_time = [[370, 510], [1055, 1195]]
# specific_time = [[1055, 1195]]
# specific_time = [[20, 140], [190, 346], [370, 1000], [1055, 1195]] #all fit
# specific_time = [[20, 140], [375, 495], [1055, 1175]] #120hour fit
# specific_time = [[375, 1000]]
specific_time = []
first_fp = 375
divide = 72
time_range = 120
last_time = 1000
while first_fp < last_time - time_range:
    specific_time.append([first_fp, first_fp + time_range])
    first_fp += divide

# V to P 一次変換式の傾き(a)と切片(b)
a = 497.74
b = -1492.3


def getNearestIndex(input_list, num):
    # リスト要素と対象値の差分を計算し最小値のインデックスを取得
    idx = np.abs(np.asarray(input_list) - num).argmin()
    return idx


def getNearestValue(input_list, num):
    idx = np.abs(np.asarray(input_list) - num).argmin()
    return input_list[idx]


# fitting用関数
def nonlinear_fit(x, a, b):
    return b * np.exp(-a * x)


# マウスカーソルがあるところに垂直線を表示
def motion(event):
    x = event.xdata
    cur_v.set_xdata(x)
    plt.draw()


# マウスを押したら垂直線を固定で表示
def onclick(event):
    global click_count
    global xvline_list
    global cmap
    print('click num: {}, click: button={}, x={}, y={}, xdata={}, ydata={}'.format(click_count, event.button,
                                                                    event.x, event.y, event.xdata, event.ydata))
    ax.axvline(x=event.xdata, c=cmap(int((click_count % 8) / 2)))
    plt.draw()
    xvline_list.append(event.xdata)
    click_count += 1
    if click_count % 2 == 0:
        time.sleep(0.1)
        plt.close()


csvpath = '//Users//minamihideyuki//data//lab//for_Australia//pressure_chech'

dt_now = datetime.datetime.now()
dt_now_str = dt_now.strftime('%Y%m%d')

if cut_mode == 0:
    out_dir = os.path.join(csvpath, 'plot_and_data', vol_name[:-4] + 'in' + dt_now_str + '_all')
elif cut_mode == 1 or 2:
    out_dir = os.path.join(csvpath, 'plot_and_data', vol_name[:-4] + 'in' + dt_now_str + '_cut')
else:
    sys.exit('cut_mode error')
if not os.path.exists(out_dir):
    os.makedirs(out_dir, exist_ok=True)

vol_path = os.path.join(csvpath, vol_name)
atm_ondotori_path = os.path.join(csvpath, atm_ondotori_name)
temp_ondotori_path = os.path.join(csvpath, temp_ondotori_name)

out_atm_ondotori = os.path.join(out_dir, '{}_edit_{}.csv'.format(atm_ondotori_name[:-4], dt_now_str))
out_temp_ondotori = os.path.join(out_dir, '{}_edit_{}.csv'.format(temp_ondotori_name[:-4], dt_now_str))
output_filepath = os.path.join(out_dir, 'dff_press_edit{}.csv'.format(dt_now_str))
output_pdf = os.path.join(out_dir, 'dff_press_plot{}.pdf'.format(dt_now_str))
out_csv_path = os.path.join(out_dir, 'fitting_data{}.csv'.format(dt_now_str))
out_xvline_path = os.path.join(out_dir, 'xvline_data{}.csv'.format(dt_now_str))

shutil.copy(vol_path, out_dir)

# fileの存在確認
if not os.path.exists(vol_path):
    sys.exit('there is no \"voltage\" file: {}'.format(vol_path))
if not os.path.exists(atm_ondotori_path):
    sys.exit('there is no \"atm_ondotori\" file: {}'.format(atm_ondotori_path))
if not os.path.exists(temp_ondotori_path):
    sys.exit('there is no \"temp ondotori\" file: {}'.format(temp_ondotori_path))

# V to P 計算
####################
vol_pn = pn.read_csv(vol_path)
vol_pn = vol_pn.drop(vol_pn.index[0:2])
vol_pn = vol_pn.drop(columns=['Date/Time.1', 'No.2', 'No.3', 'No.4'])
vol_pn = vol_pn[vol_pn['No.1'].astype('float') > 3.1]
vol_pn = vol_pn.reset_index(drop=True)

pressure = []
press_time = []
elapsed_time = []
press_time_unix = []
first_time = datetime.datetime.strptime(vol_pn['Date/Time'][0], '%Y-%m-%d %H:%M:%S')

for i in range(0, len(vol_pn)):
    p_tmp = a * float(vol_pn['No.1'][i]) + b
    time_t = datetime.datetime.strptime(vol_pn['Date/Time'][i], '%Y-%m-%d %H:%M:%S')
    if cut_mode == 1:
        if time_t < cut_time:
            continue
    if cut_mode == 2:
        if time_t < cut_time or time_t > cut_time2:
            continue
    pressure.append(p_tmp)
    press_time.append(time_t)
    elapsed_time.append(((time_t - first_time).total_seconds()) / 3600)
    press_time_unix.append(datetime.datetime.strptime(vol_pn['Date/Time'][i], '%Y-%m-%d %H:%M:%S').timestamp())

vol_pn = vol_pn.drop(columns='Date/Time')
vol_pn = vol_pn.drop(vol_pn.index[0:len(vol_pn) - len(press_time)])
vol_pn['time'] = press_time
vol_pn['pressure'] = pressure
vol_pn = vol_pn.reset_index(drop=True)

#####################################################
# 大気圧取得用温度取り情報取得
#####################################################


f_atm_ondotori = open(atm_ondotori_path, 'r', encoding='shift_jis')
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

# 整形してファイル出力
atm_ondotori_pn = pn.DataFrame()
atm_ondotori_pn['time'] = atm_ondotori_time
atm_ondotori_pn['temperature'] = temprature
atm_ondotori_pn['pressure'] = at_press
atm_ondotori_pn.to_csv(out_atm_ondotori, index=False)

#####################################################
# シェル内温度取り情報取得
#####################################################
temp_ondotori_pn = pn.read_csv(temp_ondotori_path)
temp_ondotori_pn = temp_ondotori_pn.drop(columns=['Group Name', 'Device Name'])
temp_ondotori_pn = temp_ondotori_pn[3:]
temp_ondotori_pn = temp_ondotori_pn.reset_index(drop=True)
temp_ondotori_time = []
temp_elasped_time = []
temp_first_time = datetime.datetime.now()
temp_ondotori_time_unix = []
for i in range(len(temp_ondotori_pn)):
    # time_t = datetime.datetime.strptime(temp_ondotori_pn['Model'][i], '%Y/%m/%d %H:%M:%S')
    time_t = datetime.datetime.strptime(temp_ondotori_pn['Model'][i], '%Y/%m/%d %H:%M:%S') + datetime.timedelta(
        minutes=30)
    if i == 0:
        temp_first_time = time_t
    temp_ondotori_time.append(time_t)
    temp_elasped_time.append(((time_t - temp_first_time).total_seconds()) / 3600)
    temp_ondotori_time_unix.append(time_t.timestamp())

temp_ondotori_pn['time'] = temp_ondotori_time
temp_ondotori_pn = temp_ondotori_pn.drop(columns=['Model'])
temp_ondotori_pn = temp_ondotori_pn.rename(columns={'Serial': 'temperature'})
temp_ondotori_pn = temp_ondotori_pn.reindex(columns=['time', 'temperature'])
temp_ondotori_pn['temperature'] = temp_ondotori_pn['temperature'].astype('float')
temp_ondotori_pn.to_csv(out_temp_ondotori, index=False)

#############################################
##plotからマウス操作で切り取りラインを取得
#############################################
fitting_point_index = []

if point_select_mode == 0:  #クリックで選択するモード
    loop_num = input('how many loops\n')
    if not loop_num.isdecimal():
        sys.exit('loop num must be \"int\"')
    loop_num = int(loop_num)

    for i in range(loop_num):
        fig = plt.figure(tight_layout=True)
        ax = fig.add_subplot(111)
        ax.plot(press_time_unix, vol_pn['pressure'], 'x', label='raw data', ms=1)
        # ax.plot(atm_elapsed_time, atm_ondotori_pn['pressure'], 'x', label='atm data', ms=1, c='r')
        ax.grid()
        ax.set_ylim(100, 1000)
        ax.set_xlim(press_time_unix[0], press_time_unix[-1])
        ax.set_yscale('log', base=10)
        ax.tick_params(axis='x', labelsize=5)
        ax.set_ylabel('pressure [hPa]')

        ax_temp = ax.twinx()
        ax_temp.plot(temp_ondotori_time_unix, temp_ondotori_pn['temperature'], 'x', label='temprerature', c='b', ms=1,
                     alpha=0.5)
        ax_temp.set_xlim(press_time_unix[0], press_time_unix[-1])
        ax_temp.set_ylabel('temperature [°C]')

        plot_xvline_list = []  # クリックした場所の一番近いデータがあるところのxポジションを記録
        if click_count != 0:
            # xvlineの情報からfitting point(first, last)を取得、elapsed timeと照合、値とindexを取得
            for i in range(0, len(xvline_list) - 1, 2):
                fp = xvline_list[i]
                lp = xvline_list[i + 1]
                plot_xvline_list.append(getNearestValue(press_time_unix, fp))
                plot_xvline_list.append(getNearestValue(press_time_unix, lp))

        # 垂直線をplot
        for i in range(len(plot_xvline_list)):
            ax.axvline(x=plot_xvline_list[i], c=cmap(int((i % 8) / 2)))

        cur_v = ax.axvline(elapsed_time[0], c=cmap(int((click_count % 8) / 2)))
        cid = fig.canvas.mpl_connect('button_press_event', onclick)
        fig.canvas.mpl_connect('motion_notify_event', motion)
        plt.show()

elif point_select_mode == 1:    #最初に選択したspecific_timeから計算
    for i in range(0, len(specific_time)):
        first_point = getNearestIndex(elapsed_time, specific_time[i][0])
        end_point = getNearestIndex(elapsed_time, specific_time[i][1])
        fitting_point_index.append([first_point, end_point])

else:
    sys.exit('point_select_mode must be 0/1')

for i in range(0, len(xvline_list) - 1, 2):
    first_point = getNearestIndex(press_time_unix, xvline_list[i])
    end_point = getNearestIndex(press_time_unix, xvline_list[i + 1])
    fitting_point_index.append([first_point, end_point])


####################################
##温度補正&output pandas作成
####################################

##時刻合わせ


output_time_v = []
output_v = []
output_raw_diff_press = []
output_fixed_dff_press = []
output_time_atm_ondotori = []
output_temp_outside = []
output_atm = []
output_time_temp_ondotori = []
output_temp_shell = []
atm_first_point = 0
temp_first_point = 0
fix_press_list = []
tmp_num = 0

for i in range(len(fitting_point_index)):
    print('loop {}, pressure first time: {}'.format(i, vol_pn['time'][fitting_point_index[i][0]]))
    count_num = 0
    for j in range(fitting_point_index[i][0], fitting_point_index[i][1] + 1):
        time_vol_unix = press_time_unix[j]
        time_atm_index = getNearestIndex(atm_ondotori_time_unix, time_vol_unix)
        time_temp_index = getNearestIndex(temp_ondotori_time_unix, time_vol_unix)
        time_diff_atm = atm_ondotori_pn['time'][time_atm_index] - vol_pn['time'][j]
        time_diff_temp = temp_ondotori_pn['time'][time_temp_index] - vol_pn['time'][j]
        if abs(time_diff_atm.total_seconds()) > 150.0 or abs(time_diff_temp.total_seconds()) > 150.0:
            continue
        if count_num == 0:
            atm_first_point = time_atm_index
            temp_first_point = time_temp_index
            count_num += 1
        # 温度補正
        fix_press = (vol_pn['pressure'][j] + atm_ondotori_pn['pressure'][time_atm_index]) * (
                temp_ondotori_pn['temperature'][temp_first_point] + 273.16) / (
                            temp_ondotori_pn['temperature'][time_temp_index] + 273.16) - atm_ondotori_pn['pressure'][
                        atm_first_point]

        output_time_v.append(vol_pn['time'][j])
        output_v.append(vol_pn['No.1'][j])
        output_raw_diff_press.append(vol_pn['pressure'][j])
        output_fixed_dff_press.append(fix_press)
        output_time_atm_ondotori.append(atm_ondotori_pn['time'][time_atm_index])
        output_temp_outside.append(atm_ondotori_pn['temperature'][time_atm_index])
        output_atm.append(atm_ondotori_pn['pressure'][time_atm_index])
        output_time_temp_ondotori.append(temp_ondotori_pn['time'][time_temp_index])
        output_temp_shell.append(temp_ondotori_pn['temperature'][time_temp_index])

    fix_press_list.append([output_fixed_dff_press[tmp_num], output_fixed_dff_press[-1]])
    tmp_num = len(output_fixed_dff_press)

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


cut_elapsed_time = []
for i in range(len(output_time_v)):
    time_t = output_time_v[i]
    cut_elapsed_time.append(((time_t - first_time).total_seconds() / 3600))

fitting_value = [[0.0006, 275.0]]
param = []
fp = 0
lp = 0
for i in range(len(fitting_point_index)):
    if i == 0:
        fp = 0
        lp = fitting_point_index[i][1] - fitting_point_index[i][0]
    else:
        fp = lp
        lp = fp + fitting_point_index[i][1] - fitting_point_index[i][0]
    index_range = fitting_point_index[i][1] - fitting_point_index[i][0]
    param, cov = curve_fit(nonlinear_fit, elapsed_time[fitting_point_index[i][0]:fitting_point_index[i][1] + 1],
                           output_fixed_dff_press[fp:lp + 1],
                           p0=[fitting_value[0][0], fitting_value[0][1]])
    error = np.sqrt(np.diag(cov))
    fitting_value.append([param[0], param[1], error[0], error[1]])
fitting_value = fitting_value[1:]


###################################################
# plot
###################################################

out_pdf = PdfPages(output_pdf)

fig = plt.figure(tight_layout=True)
Minute_fmt = mdates.DateFormatter("%m-%d\n%H:%M")
locator = mdates.DayLocator()

ax = fig.add_subplot(111)
ax.plot(vol_pn['time'], vol_pn['pressure'], 'x', label='raw data', ms=1)
ax.xaxis.set_major_formatter(Minute_fmt)
ax.xaxis.set_major_locator(locator)
ax.legend()
ax.grid()
ax.set_ylim(100, 1000)
ax.set_yscale('log', base=10)
ax.tick_params(axis='x', labelsize=3)
out_pdf.savefig()
fig.clf()


ax = fig.add_subplot(111)
ax.plot(vol_pn['time'], vol_pn['pressure'], 'x', label='raw data', ms=1)
ax.plot(output_time_v, output_fixed_dff_press, 'x', label='fixed data', ms=1)
ax.xaxis.set_major_formatter(Minute_fmt)
ax.xaxis.set_major_locator(locator)
ax.legend()
ax.grid()
ax.set_ylim(100, 1000)
ax.set_yscale('log', base=10)
ax.tick_params(axis='x', labelsize=3)
out_pdf.savefig()
fig.clf()

##with atm pressure
#####################################
ax = fig.add_subplot(111)
ax.plot(vol_pn['time'], vol_pn['pressure'], 'x', label='raw data', ms=1)
ax.plot(output_time_v, output_fixed_dff_press, 'x', label='fixed data', ms=1)
ax.set_xlim(vol_pn['time'][0], vol_pn.iloc[-1]['time'])
ax.xaxis.set_major_formatter(Minute_fmt)
ax.xaxis.set_major_locator(locator)
ax.tick_params(axis='x', labelsize=3)
ax.set_ylabel('pressure [hPa]')
h1, l1 = ax.get_legend_handles_labels()
ax.grid()
ax.set_ylim(100, 1000)
ax.set_yscale('log', base=10)

ax_atm = ax.twinx()
ax_atm.plot(atm_ondotori_pn['time'], atm_ondotori_pn['pressure'], 'x', label='atmosphere', c='r', ms=1, alpha=0.5)
ax_atm.set_xlim(vol_pn['time'][0], vol_pn.iloc[-1]['time'])
ax_atm.xaxis.set_major_formatter(Minute_fmt)
ax_atm.xaxis.set_major_locator(locator)
ax_atm.set_ylim(900, 1000)
h2, l2 = ax_atm.get_legend_handles_labels()
ax_atm.set_xlim(vol_pn['time'][0], vol_pn.iloc[-1]['time'])

ax.legend(h1 + h2, l1 + l2, loc='upper left')
out_pdf.savefig()
fig.clf()

## raw and fixed pressure, and temperature
ax = fig.add_subplot(111)
ax.plot(vol_pn['time'], vol_pn['pressure'], 'x', label='raw data', ms=1)
ax.plot(output_time_v, output_fixed_dff_press, 'x', label='fixed data', ms=1)
ax.set_xlim(vol_pn['time'][0], vol_pn.iloc[-1]['time'])
ax.xaxis.set_major_formatter(Minute_fmt)
ax.xaxis.set_major_locator(locator)
ax.tick_params(axis='x', labelsize=3)
ax.set_ylabel('pressure [hPa]')
h1, l1 = ax.get_legend_handles_labels()
ax.grid()
ax.set_ylim(100, 1000)
ax.set_yscale('log', base=10)

ax_temp = ax.twinx()
ax_temp.plot(temp_ondotori_pn['time'], temp_ondotori_pn['temperature'], 'x', label='temprerature', c='b', ms=1,
             alpha=0.5)
ax_temp.set_xlim(vol_pn['time'][0], vol_pn.iloc[-1]['time'])
ax_temp.xaxis.set_major_formatter(Minute_fmt)
ax_temp.xaxis.set_major_locator(locator)
ax_temp.set_ylabel('temperature [°C]')
h2, l2 = ax_temp.get_legend_handles_labels()

ax.legend(h1 + h2, l1 + l2, loc='upper left')
out_pdf.savefig()
fig.clf()



fig = plt.figure(tight_layout=True)
Minute_fmt = mdates.DateFormatter("%m-%d\n%H:%M")
locator = mdates.DayLocator()
ax = fig.add_subplot(111)
ax.plot(vol_pn['time'], vol_pn['pressure'], 'x', label='raw data', ms=1)
ax.plot(output_time_v, output_fixed_dff_press, 'x', label='fixed data', ms=1)
ax.xaxis.set_major_formatter(Minute_fmt)
ax.xaxis.set_major_locator(locator)
for i in range(len(fitting_point_index)):
    first_index = fitting_point_index[i][0]
    end_index = fitting_point_index[i][1]
    ax.axvline(x=press_time[first_index], c=cmap(i % 20), alpha=0.4)
    ax.axvline(x=press_time[end_index], c=cmap(i % 20), alpha=0.4)
ax.legend()
ax.grid()
ax.set_ylim(100, 1000)
ax.set_yscale('log', base=10)
ax.tick_params(axis='x', labelsize=3)
out_pdf.savefig()
fig.clf()

##with atm pressure
#####################################
ax = fig.add_subplot(111)
ax.plot(vol_pn['time'], vol_pn['pressure'], 'x', label='raw data', ms=1)
ax.plot(output_time_v, output_fixed_dff_press, 'x', label='fixed data', ms=1)
ax.set_xlim(vol_pn['time'][0], vol_pn.iloc[-1]['time'])
ax.xaxis.set_major_formatter(Minute_fmt)
ax.xaxis.set_major_locator(locator)
for i in range(len(fitting_point_index)):
    first_index = fitting_point_index[i][0]
    end_index = fitting_point_index[i][1]
    ax.axvline(x=press_time[first_index], c=cmap(i % 20), alpha=0.4)
    ax.axvline(x=press_time[end_index], c=cmap(i % 20), alpha=0.4)
ax.tick_params(axis='x', labelsize=3)
ax.set_ylabel('pressure [hPa]')
h1, l1 = ax.get_legend_handles_labels()
ax.grid()
ax.set_ylim(100, 1000)
ax.set_yscale('log', base=10)

ax_atm = ax.twinx()
ax_atm.plot(atm_ondotori_pn['time'], atm_ondotori_pn['pressure'], 'x', label='atmosphere', c='r', ms=1, alpha=0.5)
ax_atm.set_xlim(vol_pn['time'][0], vol_pn.iloc[-1]['time'])
ax_atm.xaxis.set_major_formatter(Minute_fmt)
ax_atm.xaxis.set_major_locator(locator)
ax_atm.set_ylim(900, 1000)
h2, l2 = ax_atm.get_legend_handles_labels()
ax_atm.set_xlim(vol_pn['time'][0], vol_pn.iloc[-1]['time'])

ax.legend(h1 + h2, l1 + l2, loc='upper left')
out_pdf.savefig()
fig.clf()

## raw and fixed pressure, and temperature
ax = fig.add_subplot(111)
ax.plot(vol_pn['time'], vol_pn['pressure'], 'x', label='raw data', ms=1)
ax.plot(output_time_v, output_fixed_dff_press, 'x', label='fixed data', ms=1)
ax.set_xlim(vol_pn['time'][0], vol_pn.iloc[-1]['time'])
for i in range(len(fitting_point_index)):
    first_index = fitting_point_index[i][0]
    end_index = fitting_point_index[i][1]
    ax.axvline(x=press_time[first_index], c=cmap(i % 20), alpha=0.4)
    ax.axvline(x=press_time[end_index], c=cmap(i % 20), alpha=0.4)
ax.xaxis.set_major_formatter(Minute_fmt)
ax.xaxis.set_major_locator(locator)
ax.tick_params(axis='x', labelsize=3)
ax.set_ylabel('pressure [hPa]')
h1, l1 = ax.get_legend_handles_labels()
ax.grid()
ax.set_ylim(100, 1000)
ax.set_yscale('log', base=10)

ax_temp = ax.twinx()
ax_temp.plot(temp_ondotori_pn['time'], temp_ondotori_pn['temperature'], 'x', label='temprerature', c='b', ms=1,
             alpha=0.5)
ax_temp.set_xlim(vol_pn['time'][0], vol_pn.iloc[-1]['time'])
ax_temp.xaxis.set_major_formatter(Minute_fmt)
ax_temp.xaxis.set_major_locator(locator)
ax_temp.set_ylabel('temperature [°C]')
h2, l2 = ax_temp.get_legend_handles_labels()

ax.legend(h1 + h2, l1 + l2, loc='upper left')
out_pdf.savefig()
fig.clf()

ax = fig.add_subplot(111)
ax.plot(elapsed_time, vol_pn['pressure'], 'x', label='raw data', ms=1)
ax.plot(cut_elapsed_time, output_fixed_dff_press, 'x', label='fixed data', ms=1)
for i in range(0, len(fitting_value)):
    fitting_y = fitting_value[i][1] * np.exp(-fitting_value[i][0] * np.asarray(elapsed_time))
    ax.plot(elapsed_time, fitting_y, '--', alpha=0.7, c=cmap(i % 20), label='fitting{}'.format(i))
# ax.legend()
ax.grid()
ax.set_ylim(100, 1000)
ax.set_yscale('log', base=10)
ax.tick_params(axis='x', labelsize=3)
ax.set_xlabel('elapsed time [hour]')
ax.set_ylabel('pressure [hPa]')
out_pdf.savefig()
fig.clf()


ax_atm = fig.add_subplot(111)
ax_atm.plot(atm_ondotori_pn['time'], atm_ondotori_pn['pressure'], 'x', label='atmosphere', c='r', ms=1, alpha=0.5)
ax_atm.xaxis.set_major_formatter(Minute_fmt)
ax_atm.xaxis.set_major_locator(locator)
ax_atm.tick_params(axis='x', labelsize=2)
ax_atm.set_ylim(940, 960)
ax_atm.set_xlim(atm_ondotori_pn.iloc[0]['time'], atm_ondotori_pn.iloc[-1]['time'])
ax_atm.set_ylabel('pressure [hPa]')
ax_atm.grid()
out_pdf.savefig()
fig.clf()

ax_temp = fig.add_subplot(111)
ax_temp.plot(temp_ondotori_pn['time'], temp_ondotori_pn['temperature'], 'x', label='temprerature', c='b', ms=1,
             alpha=0.5)
ax_temp.xaxis.set_major_formatter(Minute_fmt)
ax_temp.xaxis.set_major_locator(locator)
ax_temp.set_ylim(10, 45)
ax_temp.set_xlim(temp_ondotori_pn.iloc[0]['time'], temp_ondotori_pn.iloc[-1]['time'])
ax_temp.tick_params(axis='x', labelsize=2)
ax_temp.set_ylabel('temperature [°C]')
ax_temp.grid()
out_pdf.savefig()
fig.clf()

out_pdf.close()

print(fitting_value)
print(len(fitting_value))
f = open(out_csv_path, 'w')
f_line = csv.writer(f)
f_line.writerow(['first point(elapsed time)', 'end point(elapsed time)', 'first point(list num)', 'end point(list num)', 'fixed press (first)', 'fixed press(end)', '1/a', '1/a error', 'time constant', 'time cons. error', 'initial value', 'initial val. error'])
for i in range(len(fitting_point_index)):
    fp_index = fitting_point_index[i][0]
    ep_index = fitting_point_index[i][1]
    fp_elapsed = elapsed_time[fp_index]
    ep_elapsed = elapsed_time[ep_index]
    press_f = fix_press_list[i][0]
    press_e = fix_press_list[i][1]
    fit_a = fitting_value[i][0]
    fit_a_err = fitting_value[i][2]
    time_const = 1 / fitting_value[i][0]
    time_const_err = fitting_value[i][2] * time_const * time_const
    initial_value = fitting_value[i][1]
    initial_value_err = fitting_value[i][3]
    f_line.writerow([fp_elapsed, ep_elapsed, fp_index, ep_index, press_f, press_e, fit_a, fit_a_err, time_const, time_const_err, initial_value, initial_value_err])

f.close()

subprocess.run(["open {}".format(output_pdf)], shell=True)
