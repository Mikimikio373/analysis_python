import subprocess
import pandas as pn
import sys
import numpy as np
import os
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib import ticker
import datetime
from matplotlib.backends.backend_pdf import PdfPages
import shutil

cut_mode = 1
# cut_time = datetime.datetime(2023, 4, 29, hour=9, minute=0, second=0)
cut_time = datetime.datetime(2023, 4, 30, hour=0, minute=0, second=0)
# cut_time = datetime.datetime(2023, 3, 4, hour=0, minute=0, second=0)
# cut_time2 = datetime.datetime(2023, 3, 5, hour=0, minute=0, second=0)


def draw_hline(ax, index):
    if index == 'ax2-ax1':
        ax.axhline(y=-0.02727, c='r', alpha=0.5)
        ax.axhline(y=-0.02872, c='r', alpha=0.5)
    if index == 'ay2-ay1':
        ax.axhline(y=0.001995, c='r', alpha=0.5)
        ax.axhline(y=0.007632, c='r', alpha=0.5)
    if index == 'ax3-ax1':
        ax.axhline(y=-0.01578, c='r', alpha=0.5)
        ax.axhline(y=-0.01893, c='r', alpha=0.5)
    if index == 'ay3-ay1':
        ax.axhline(y=0.0007324, c='r', alpha=0.5)
        ax.axhline(y=0.00385, c='r', alpha=0.5)
    if index == 'ax3-ax2':
        ax.axhline(y=0.01149, c='r', alpha=0.5)
        ax.axhline(y=0.009794, c='r', alpha=0.5)
    if index == 'ay3-ay2':
        ax.axhline(y=-0.001263, c='r', alpha=0.5)
        ax.axhline(y=-0.003781, c='r', alpha=0.5)


# plotする自作関数
def plot_angle(fig, pdfdata, pndata, index, cmap, cmap_num):
    global cut_mode
    global index_y_list
    y_mean = np.mean(np.asarray(pndata[index]))
    y_min = y_mean - 0.001
    y_max = y_mean + 0.001
    ax = fig.add_subplot(111)
    ax.scatter('time', index, data=pndata, marker='o', lw=0.5, facecolor='None', edgecolors=cmap(int(cmap_num % 10)),
               s=1.5)
    # ax.axvline(x=datetime.datetime(2023, 4, 3, hour=9, minute=0, second=0), c='r', alpha=0.5)
    # ax.axvline(x=datetime.datetime(2023, 4, 5, hour=10, minute=30, second=0), c='b', alpha=0.5)
    # ax.axvline(x=datetime.datetime(2023, 4, 4, hour=15, minute=46, second=0), c='b', alpha=0.5)
    # ax.axvline(x=datetime.datetime(2023, 4, 6, hour=13, minute=15, second=0), c='b', alpha=0.5)
    # ax.axvline(x=datetime.datetime(2023, 4, 7, hour=15, minute=14, second=0), c='b', alpha=0.5)
    # ax.axvline(x=datetime.datetime(2023, 4, 9, hour=11, minute=46, second=0), c='b', alpha=0.5)
    # ax.axvline(x=datetime.datetime(2023, 4, 12, hour=7, minute=56, second=0), c='b', alpha=0.5)
    # ax.axvline(x=datetime.datetime(2023, 4, 21, hour=19, minute=23, second=20), c='b', alpha=0.5)
    # ax.axvline(x=datetime.datetime(2023, 4, 21, hour=22, minute=10, second=00), c='b', alpha=0.5)
    # ax.axvline(x=datetime.datetime(2023, 4, 22, hour=0, minute=56, second=40), c='b', alpha=0.5)
    # ax.axvline(x=datetime.datetime(2023, 4, 22, hour=1, minute=40, second=00), c='b', alpha=0.5)
    ax.axvline(x=datetime.datetime(2023, 4, 30, hour=3, minute=16, second=40), c='b', alpha=0.5)
    # draw_hline(ax, index)
    ax.set_title(index, fontsize=15)
    ax.set_xlim(np.asarray(pndata['time'])[0], np.asarray(pndata['time'])[-1])
    Minute_fmt = mdates.DateFormatter("%m-%d\n%H:%M")
    # Minute_fmt = mdates.DateFormatter("%m-%d")
    locator = mdates.DayLocator()
    ax.xaxis.set_major_formatter(Minute_fmt)
    if cut_mode == 0:
        ax.xaxis.set_major_locator(locator)
    ax.set_ylabel('[rad]')
    ax.set_ylim(y_min, y_max)
    ax.minorticks_on()
    ax.grid(linestyle='dotted', c='k', linewidth=1)
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right")
    ax.tick_params(axis='x', labelsize=5)
    pdfdata.savefig()
    fig.clf()
    cmap_num += 1
    return cmap_num


root_path = '/Users/minamihideyuki/data/lab/lab_project/root/MakeRootFile4Keishakei.C'
print(len(sys.argv))
# error処理(コマンドライン引数について)
if len(sys.argv) != 2:
    sys.exit('command line error, please input csv path')
# コマンドライン引数の取得
path = sys.argv[1]

if cut_mode == 0:
    outdir = path[:-4]
elif cut_mode == 1 or 2:
    outdir = path[:-4] + '_cut'
else:
    sys.exit('cut_mode must be 0, 1 or 2')
os.makedirs(outdir, exist_ok=True)
shutil.copy(path, outdir)
# 出力csvのディレクトリ及び名前
edit_path = os.path.join(outdir, 'edit_data.csv')
# 出力pdfのディレクトり及び名前
pdf_path = os.path.join(outdir, 'plot.pdf')
print(path)
print(edit_path)
print(pdf_path)

# error処理(入力したパスがあるかの存在確認)
if not os.path.exists(path):
    sys.exit('there are not tha path :{}'.format(path))

# csv to pandas
input = pn.read_csv(path)
# いらない列の削除
input = input.drop(input.index[0:2])
input = input.drop(columns=['No.7', 'No.8'])
input = input.reset_index(drop=True)
print(len(input))

# 記録電圧が2Vより小さいものは削除
input = input[input['No.1'].astype('float') > 2]
input = input.reset_index(drop=True)
print(len(input))

a = 0.2167
b = 0.5432

ax1 = []
ay1 = []
ax2 = []
ay2 = []
ax3 = []
ay3 = []
time_all = []

# 電圧 to 角度
for i in range(0, len(input)):
    if cut_mode == 1:
        if datetime.datetime.strptime(input['Date/Time'][i], '%Y-%m-%d %H:%M:%S') < cut_time:
            continue
    if cut_mode == 2:
        if datetime.datetime.strptime(input['Date/Time'][i], '%Y-%m-%d %H:%M:%S') < cut_time or datetime.datetime.strptime(input['Date/Time'][i], '%Y-%m-%d %H:%M:%S') > cut_time2:
            continue
    tan1 = a * float(input['No.1'][i]) - b
    tan2 = a * float(input['No.2'][i]) - b
    tan3 = a * float(input['No.3'][i]) - b
    tan4 = a * float(input['No.4'][i]) - b
    tan5 = a * float(input['No.5'][i]) - b
    tan6 = a * float(input['No.6'][i]) - b
    ax1.append(tan2)
    ay1.append(-tan1)
    ax2.append(-tan4)
    ay2.append(tan3)
    ax3.append(-tan5)
    ay3.append(-tan6)
    time_all.append(datetime.datetime.strptime(input['Date/Time'][i], '%Y-%m-%d %H:%M:%S'))

if cut_mode == 1 or cut_mode == 2:
    input = input.drop(input.index[0:len(input) - len(time_all)])
    input = input.reset_index(drop=True)
# pandasにlistの追加
input['time'] = time_all
input['ax1'] = np.asarray(ax1)
input['ay1'] = np.asarray(ay1)
input['ax2'] = np.asarray(ax2)
input['ay2'] = np.asarray(ay2)
input['ax3'] = np.asarray(ax3)
input['ay3'] = np.asarray(ay3)
input['ax1-ax2'] = np.asarray(input['ax1'] - input['ax2'])
input['ay1-ay2'] = np.asarray(input['ay1'] - input['ay2'])
input['ax1-ax3'] = np.asarray(input['ax1'] - input['ax3'])
input['ay1-ay3'] = np.asarray(input['ay1'] - input['ay3'])
input['ax2-ax3'] = np.asarray(input['ax2'] - input['ax3'])
input['ay2-ay3'] = np.asarray(input['ay2'] - input['ay3'])
input['ax2-ax1'] = np.asarray(input['ax2'] - input['ax1'])
input['ay2-ay1'] = np.asarray(input['ay2'] - input['ay1'])
input['ax3-ax1'] = np.asarray(input['ax3'] - input['ax1'])
input['ay3-ay1'] = np.asarray(input['ay3'] - input['ay1'])
input['ax3-ax2'] = np.asarray(input['ax3'] - input['ax2'])
input['ay3-ay2'] = np.asarray(input['ay3'] - input['ay2'])

# plot
fig = plt.figure(tight_layout=True)
cmap_num = 0
cmap = plt.get_cmap("tab10")
out_pdf = PdfPages(pdf_path)
for i in range(1, 4):
    cmap_num = plot_angle(fig, out_pdf, input, 'ax{}'.format(i), cmap, cmap_num)
for i in range(1, 4):
    cmap_num = plot_angle(fig, out_pdf, input, 'ay{}'.format(i), cmap, cmap_num)

cmap_num = plot_angle(fig, out_pdf, input, 'ax2-ax1', cmap, cmap_num)
cmap_num = plot_angle(fig, out_pdf, input, 'ay2-ay1', cmap, cmap_num)
cmap_num = plot_angle(fig, out_pdf, input, 'ax3-ax1', cmap, cmap_num)
cmap_num = plot_angle(fig, out_pdf, input, 'ay3-ay1', cmap, cmap_num)
cmap_num = plot_angle(fig, out_pdf, input, 'ax3-ax2', cmap, cmap_num)
cmap_num = plot_angle(fig, out_pdf, input, 'ay3-ay2', cmap, cmap_num)

out_pdf.close()

# 出力用にpandasの整形
droplist = ['Date/Time.1', 'time']
for i in range(1, 4):
    for j in range(1, 4):
        if i == j:
            continue
        xname = 'ax{}-ax{}'.format(i, j)
        yname = 'ay{}-ay{}'.format(i, j)
        droplist.append(xname)
        droplist.append(yname)
input = input.drop(columns=droplist)
input.to_csv(edit_path, index=False)

# rootマクロの実行
root_command = 'root -q {}\\(\\\"{}\\\"\\)'.format(root_path, edit_path)
subprocess.run(root_command, shell=True)
