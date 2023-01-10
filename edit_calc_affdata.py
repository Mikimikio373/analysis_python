import numpy as np
import sys
import os
import pandas as pn
import json
import math
import yaml
import matplotlib as mpl
from matplotlib import pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from sklearn import linear_model


def plot_data(fig, pndata, pdfdata, shihtX, shihtY, title):
    ax = fig.add_subplot(111)
    ax.scatter(x=pndata["VX"], y=pndata["VY"], marker='o', color='none', edgecolors="k", lw=0.5)
    ax.set_title('VX VY' + title)
    ax.set_xlabel('VX (steps)')
    ax.set_ylabel('VY (steps)')
    ax.set(xlim=(-1, shihtX), ylim=(-1, shihtY))
    ax.yaxis.set_major_locator(mpl.ticker.MultipleLocator())
    ax.yaxis.set_major_locator(mpl.ticker.MultipleLocator())
    pdfdata.savefig()
    fig.clf()

    ax = fig.add_subplot(111)
    ax.scatter(x=pndata["dsx"], y=pndata["dsy"], marker='o', color='none', edgecolors="y", lw=0.5)
    ax.set_title('stage dX dY' + title)
    ax.set_xlabel('dX [mm]')
    ax.set_ylabel('dY [mm]')
    pdfdata.savefig()
    fig.clf()

    ax = fig.add_subplot(111)
    ax.scatter(x=pndata["dpx"], y=pndata["dpy"], marker='o', color='none', edgecolors="g", lw=0.5)
    ax.set_title('pixel dx dy' + title)
    ax.set_xlabel('dx [pixel]')
    ax.set_ylabel('dy [pixel]')
    pdfdata.savefig()
    fig.clf()

    ax = fig.add_subplot(111)
    ax.errorbar(x=pndata["dsx"], y=pndata["dpx"], xerr=np.full(len(pndata['dsx']), 0.005), yerr=pndata["delta_px"],
                marker='o', color='none', markeredgecolor="b", ecolor="b", lw=0.5)
    ax.set_title('distance x (stage X vs pixel x)' + title)
    ax.set_xlabel('dX [mm]')
    ax.set_ylabel('dx [pixel]')
    pdfdata.savefig()
    fig.clf()

    ax = fig.add_subplot(111)
    ax.errorbar(x=pndata["dsy"], y=pndata["dpy"], xerr=np.full(len(pndata['dsx']), 0.005), yerr=pndata["delta_py"],
                marker='o', color='none', markeredgecolor="r", ecolor="r", lw=0.5)
    ax.set_title('distance y (stage Y vs pixel y)' + title)
    ax.set_xlabel('dY [mm]')
    ax.set_ylabel('dx [pixel]')
    pdfdata.savefig()
    fig.clf()


def find_entry_cut(fig, pndata, pdfdata):
    hist = np.histogram(pndata["Entries"].values, bins=200)
    hist_min = min(hist[0])
    hist_max = max(hist[0])
    min_list = []
    #最小値のbin番号リストを取得
    for i in range(1, len(hist[0])):
        if hist[0][i] == hist_min:
            min_list.append(i)
    #最大値のbin番号を取得
    max_num = 0
    for i in range(1, len(hist[0])):
        if hist[0][i] == hist_max:
            max_num = i
            break
    if min(min_list) > max_num:
        cut = hist[1][min_list[0] + 1]
    else:
        cut = hist[1][min_list[1] + 1]
    print('entries cut is : ', cut)
    ax = fig.add_subplot(111)
    ax.hist(pndata["Entries"], bins=200)
    ax.vlines(cut, 0, max(hist[0]), "red")
    ax.set_title('Number of grains used for fitting')
    pdfdata.savefig()
    fig.clf()

    return cut



def line_fit(pndata, pdfdata, fig):  #px pyの絶対値が200以上のものを使ってfittingするといいかも
    # x fit and plot
    clf = linear_model.LinearRegression(fit_intercept=False)
    X = pndata[['dsx']].values
    Y = pndata['dpx'].values
    clf.fit(X, Y)
    coef_x = clf.coef_[0]

    ax = fig.add_subplot(111)
    ax.errorbar(x=pndata["dsx"], y=pndata["dpx"], xerr=np.full(len(pndata['dsx']), 0.005), yerr=pndata["delta_px"],
                marker='o', color='none', markeredgecolor="b", ecolor="b", lw=0.5)
    ax.set_title('distance x (stage X vs pixel x)  fitting')
    ax.set_xlabel('dX [mm]')
    ax.set_ylabel('dx [pixel]')
    ax.plot(X, clf.predict(X), label='fitting', c='b', linestyle=':', lw=0.5, marker=None)
    ax.legend()
    out_pdf.savefig()
    fig.clf()

    # y fit and plot
    X = pndata[['dsy']].values
    Y = pndata['dpy'].values
    clf.fit(X, Y)
    coef_y = clf.coef_[0]

    ax = fig.add_subplot(111)
    ax.errorbar(x=pndata["dsy"], y=pndata["dpy"], xerr=np.full(len(pndata['dsy']), 0.005), yerr=pndata["delta_py"],
                marker='o', color='none', markeredgecolor="r", ecolor="r", lw=0.5)
    ax.set_title('distance y (stage Y vs pixel y)  fitting')
    ax.set_xlabel('dY [mm]')
    ax.set_ylabel('dx [pixel]')
    ax.plot(X, clf.predict(X), label='fitting', c='r', linestyle=':', lw=0.5, marker=None)
    ax.legend()
    out_pdf.savefig()
    fig.clf()

    return coef_x, coef_y


def calc_aff(pndata):
    px = pndata['dpx'].values.astype(np.longdouble)
    py = pndata['dpy'].values.astype(np.longdouble)
    sx = pndata['dsx'].values.astype(np.longdouble)
    sy = pndata['dsy'].values.astype(np.longdouble)
    px_square = np.sum(np.square(px, dtype=np.longdouble))
    py_square = np.sum(np.square(py, dtype=np.longdouble))
    pxy = np.sum(px * py, dtype=np.longdouble)
    pxsx = np.sum(px * sx, dtype=np.longdouble)
    pxsy = np.sum(px * sy, dtype=np.longdouble)
    pysx = np.sum(py * sx, dtype=np.longdouble)
    pysy = np.sum(py * sy, dtype=np.longdouble)

    a = (pxsx * py_square - pysx * pxy) / (px_square * py_square - pxy * pxy)
    b = (pxsx * pxy - pysx * px_square) / (pxy * pxy - px_square * py_square)
    c = (pxsy * py_square - pysy * pxy) / (px_square * py_square - pxy * pxy)
    d = (pxsy * pxy - pysy * px_square) / (pxy * pxy - px_square * py_square)
    print(a, b, c, d)
    return a, b, c, d


args = sys.argv
if not len(args) == 5:
    sys.exit('command line error, please input \"path vx vy npicture\"')
areapath = args[1]
view_x = int(args[2])
view_y = int(args[3])
npicture = int(args[4])
print('target dir: {}'.format(areapath))
if not os.path.exists(areapath):
    sys.exit("there are not direcory: {}".format(areapath))
fit_csv = os.path.join(areapath, 'GrainMatching_loop/fitdata.csv')

fit_pn = pn.read_csv(fit_csv, header=0)
# エンコーダ情報の取得
dsX_all = []
dsY_all = []
delta_px_all = []
delta_py_all = []
n = 0
view = 0

# jsonファイル参照して、ファイル成型
drop_line = []
for i in range(0, len(fit_pn)):
    if fit_pn['Entries'][i] == 0:  # entriesが0のエラー処理
        drop_line.append(i)
        delta_px = 0
        delta_py = 0
    else:
        delta_px = fit_pn['sigmapx'][i] / math.sqrt(fit_pn['Entries'][i])
        delta_py = fit_pn['sigmapy'][i] / math.sqrt(fit_pn['Entries'][i])
    delta_px_all.append(delta_px)
    delta_py_all.append(delta_py)

    # フィッティングした時のシグマ値とエントリーから誤差を計算
    vx = fit_pn['VX'][i]
    vy = fit_pn['VY'][i]

    if vy == 0:
        view_base = 0
    else:
        view_base = (view_x + 1) * vy - 1
    base_json_path = areapath + '/IMAGE00_AREA-1/V{:08}_L0_VX0000_VY0000_0_{:03}.json'.format(view_base,
                                                                                              npicture)
    if vy == 0:
        view = view_base = vx
    else:
        view = view_base + vx + 1
    json_path = areapath + '/IMAGE00_AREA-1/V{:08}_L0_VX{:04}_VY{:04}_0_{:03}.json'.format(view, vx, vy,
                                                                                           npicture)
    # スキャンデータがない時の処理
    if not os.path.exists(base_json_path):
        print('error! there is not base_json_path')
        sys.exit()
    if not os.path.exists(json_path):
        print('json not exist: ', json_path)
        dsX = 'none'
        dsY = 'none'
        dsX_all.append(dsX)
        dsX_all.append(dsY)
        continue

    base_json = open(base_json_path, 'r')
    json_open = open(json_path, 'r')
    j = json.load(json_open)
    base_j = json.load(base_json)
    base_json.close()
    json_open.close()

    base_sX = base_j['Images'][0]['x']
    base_sY = base_j['Images'][0]['y']
    sX = j['Images'][0]['x']
    sY = j['Images'][0]['y']

    dsX = sX - base_sX
    dsY = sY - base_sY
    # dsX = base_sX - sX
    # dsY = base_sY - sY

    # print(dsX, dsY)

    dsX_all.append(dsX)
    dsY_all.append(dsY)

fit_pn['dsx'] = dsX_all
fit_pn['dsy'] = dsY_all
fit_pn['delta_px'] = delta_px_all
fit_pn['delta_py'] = delta_py_all
fit_pn = fit_pn.drop(fit_pn.index[drop_line])
fit_pn = fit_pn.reset_index(drop=True)
n_total = len(fit_pn)
print(len(fit_pn))

# pdf file open
outpath = os.path.join(areapath, "edit_fitting_data.pdf")
out_pdf = PdfPages(outpath)

fig = plt.figure(tight_layout=True)

# 処理なしのplot
plot_data(fig, fit_pn, out_pdf, view_x, view_y, '')

entries_cut = find_entry_cut(fig, fit_pn, out_pdf)
# フィッティングできていなさそうなところをカット
drop_line = []
for j in range(0, len(fit_pn)):
    if fit_pn['Entries'][j] < entries_cut:
        drop_line.append(j)
fit_pn = fit_pn.drop(fit_pn.index[drop_line])
fit_pn = fit_pn.reset_index(drop=True)
n_cut1 = len(fit_pn)
print(len(fit_pn))

fit_pn.to_csv(os.path.join(areapath, 'GrainMatching_loop', 'fitdata_firstcut.csv'))
# 簡単処理後のplot
plot_data(fig, fit_pn, out_pdf, view_x, view_y, '  first cut')

# 直線fitting
coef_x, coef_y = line_fit(fit_pn, out_pdf, fig)

# fitting情報からnoiseの除去
drop_line = []
for k in range(0, len(fit_pn)):
    if abs(fit_pn['dpx'][k] - coef_x * fit_pn['dsx'][k]) > 50 or abs(fit_pn['dpy'][k] - coef_y * fit_pn['dsy'][k]) > 25:
        drop_line.append(k)
fit_pn = fit_pn.drop(fit_pn.index[drop_line])
fit_pn = fit_pn.reset_index(drop=True)
n_cut2 =len(fit_pn)
print(len(fit_pn))
plot_data(fig, fit_pn, out_pdf, view_x, view_y, '  fitting cut')

# affine parameterの計算
aff_a, aff_b, aff_c, aff_d = calc_aff(fit_pn)

# pdf file close
out_pdf.close()

fit_pn.to_csv(areapath + '/GrainMatching_loop/fitdata_edit.csv')

out_data_path = os.path.join(areapath, "aff_data.csv")
out_data = open(out_data_path, 'w')
out_data.write('total,cut1,cut2,a,b,c,d\n')
out_data.write('{},{},{},{},{},{},{}'.format(n_total,n_cut1,n_cut2,aff_a,aff_b,aff_c,aff_d))
out_data.close()
