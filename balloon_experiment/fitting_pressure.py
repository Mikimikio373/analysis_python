import csv
from scipy.optimize import curve_fit
import pandas as pn
import numpy as np
import os
import sys
import datetime
import matplotlib.pyplot as plt
import time

basepath = '/Users/minamihideyuki/data/lab/for_Australia/pressure_chech/'
file_data = '20230328'
out_dir = os.path.join(basepath, 'plot_and_data')
input_path = os.path.join(out_dir, 'dff_press_edit{}.csv'.format(file_data))
if not os.path.exists(out_dir):
    os.makedirs(out_dir)
out_pdf_path = os.path.join(out_dir, 'fitting_plot_{}.pdf'.format(file_data))
out_csv_path = os.path.join(out_dir, 'fitting_data_{}.csv'.format(file_data))

#最初にfig, axを準備
fig = plt.figure(tight_layout=True)
ax = fig.add_subplot(111)
click_count = 0  #クリックした回数
xvline_list = [] #クリックした場所の、xポジションを記録
cmap = plt.get_cmap('Set1')
cur_v = ax.axvline(-1, c=cmap(int((click_count % 8) / 2)))
fitting_value = []

def getNearestIndex(list, num):
    # リスト要素と対象値の差分を計算し最小値のインデックスを取得
    idx = np.abs(np.asarray(list) - num).argmin()
    return idx

#fitting用関数
def nonlinear_fit(x, a, b):
    return b * np.exp(-a * x)

#マウスカーソルがあるところに垂直線を表示
def motion(event):
    x = event.xdata
    cur_v.set_xdata(x)
    plt.draw()

#マウスを押したら垂直線を固定で表示
def onclick(event):
    global click_count
    global xvline_list
    global cmap
    print('click: button={}, x={}, y={}, xdata={}, ydata={}'.format(event.button,
         event.x, event.y, event.xdata, event.ydata))
    ax.axvline(x=event.xdata, c=cmap(int((click_count % 8) / 2)))
    plt.draw()
    xvline_list.append(event.xdata)
    click_count += 1
    print(click_count)
    if click_count % 2 == 0:
        time.sleep(1)
        plt.close()


if not os.path.exists(input_path):
    sys.exit('there are no file: {}'.format(input_path))

input_pn = pn.read_csv(input_path)
vol_time = []
#読み込んだファイルから経過時間を計算するためにdatetimeで抽出
for i in range(len(input_pn)):
    vol_time.append(datetime.datetime.strptime(input_pn['v recorder time'][i], '%Y-%m-%d %H:%M:%S'))

#経過時間をhourで取得
elapsed_time = []
for i in range(len(input_pn)):
    tmp_time = vol_time[i] - vol_time[0]
    elapsed_time.append(float(tmp_time.total_seconds()/3600))

# #もし時間が途切れているところがあれば、それを検索、表示
# gap_point = []
# for i in range(len(elapsed_time) - 1):
#     if elapsed_time[i + 1] - elapsed_time[i] != 300 / 3600:
#         gap_point.append(i)
#         print('detect time gap, from \"{}\" to \"{}\"\nelpsed time: {} [s], point num: {}/{}'
#               .format(vol_time[i], vol_time[i + 1], elapsed_time[i+1] - elapsed_time[i], i, len(elapsed_time)))


#plot
while True:
    #まだ一度もクリックしていなかったらTrue
    if click_count == 0:
        loop_check = True
        print('please click 2 times, \"first position\" and \"last positon\"')

    #一度クリックしていたら、fig,axを再定義して、続けるか確認
    else:
        fig = plt.figure(tight_layout=True)
        ax = fig.add_subplot(111)
        answer_s = input('Do you want to continue to fitting? y/n \n')
        if answer_s == 'y':
            loop_check = True
            print('please click 2 times, \"first position\" and \"last positon\"')
        elif answer_s == 'n':
            loop_check = False
        else:
            sys.exit('please answer \'y\' or \'n\'')
    #fixed pressureをplot
    ax.plot(elapsed_time, input_pn['fixed dff pressure'], 'x', ms=1, label='diff P')
    ax.set_ylim(100, 1000)
    ax.set_xlabel('elapsed time [hour]')
    ax.set_ylabel('differential pressure [hPa]')
    ax.set_yscale('log', base=10)
    ax.grid()

    #クリックされていたら、フィッティングをしてプロット
    plot_xvline_list = []  # クリックした場所の一番近いデータがあるところのxポジションを記録
    if click_count != 0:
        fitpoint_index = []
        #xvlineの情報からfitting point(first, last)を取得、elapsed timeと照合、値とindexを取得
        for i in range(0, len(xvline_list) - 1, 2):
            fp = xvline_list[i]
            lp = xvline_list[i + 1]
            fp_index = getNearestIndex(elapsed_time, fp)
            lp_index = getNearestIndex(elapsed_time, lp)
            fitpoint_index.append([fp_index, lp_index])
            plot_xvline_list.append(elapsed_time[fp_index])
            plot_xvline_list.append(elapsed_time[lp_index])

        fitting_value = [[0.0006, 275.0]]
        #取得した範囲情報から、範囲を絞ってfitting
        for i in range(int(len(xvline_list)/2)):
            param, cov = curve_fit(nonlinear_fit, elapsed_time[fitpoint_index[i][0]:fitpoint_index[i][1]],
                                   input_pn['fixed dff pressure'][fitpoint_index[i][0]:fitpoint_index[i][1]].values,
                                   p0=[fitting_value[-1][0], fitting_value[-1][1]])
            print(param[0], param[1])
            fitting_value.append([param[0], param[1]])
            fitting_y = param[1] * np.exp(-param[0] * np.array(elapsed_time))
            ax.plot(elapsed_time, fitting_y, '--', alpha=0.5, c=cmap(i), label='fitting{}'.format(i))

    #垂直線をplot
    for i in range(len(plot_xvline_list)):
        ax.axvline(x=plot_xvline_list[i], c=cmap(int((i % 8) / 2)))

    plt.legend()
    plt.savefig(out_pdf_path, dpi=300)

    #loop checkでcontinueした場合cur_vを再定義して、再度選択モードへ
    if loop_check:
        if click_count != 0:
            cur_v = ax.axvline(-1, c=cmap(int((click_count % 8) / 2)))
        cid = fig.canvas.mpl_connect('button_press_event', onclick)
        fig.canvas.mpl_connect('motion_notify_event', motion)
    plt.show()

    if not loop_check:
        print(plot_xvline_list)
        print(len(plot_xvline_list))
        print(fitting_value)
        print(len(fitting_value))
        f = open(out_csv_path, 'w')
        f_line = csv.writer(f)
        f_line.writerow(['first point', 'end point', 'time constant', 'initial value'])
        for i in range(int(len(plot_xvline_list) / 2)):
            f_line.writerow([plot_xvline_list[i], plot_xvline_list[i + 1], fitting_value[i + 1][0], fitting_value[i + 1][1]])
        f.close()
        break


