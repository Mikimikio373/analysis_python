import json
import os.path
from statistics import mean
import sys

import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages


def plot_vec(fig, pdf: PdfPages, X: list, Y: list, U: list, V: list, title: str, factor: float, *, width :float = 1, guide: float = 0.001, min_xrange: float = 18):
    ax = fig.add_subplot(111)
    ax.quiver(X, Y, U, V, angles='xy', scale_units='xy', scale=1, units='xy', width=width)
    x = min(X) - (max(X) - min(X)) * 0.05
    y = min(Y) - (max(Y) - min(Y)) * 0.05
    ax.quiver(x, y, guide * factor, 0, angles='xy', scale_units='xy', scale=1, units='xy', width=width)
    ax.quiver(x, y, 0, guide * factor, angles='xy', scale_units='xy', scale=1, units='xy', width=width)
    ax.text(x, y, f" {guide * 1000} um", va="bottom", ha="left")
    if max(X) - min(X) < min_xrange:
        ax.set_xlim(mean(X) - min_xrange, mean(X) + min_xrange)
    ax.set_title(title)
    ax.set_xlabel("Stage X [mm]")
    ax.set_ylabel("Stage Y [mm]")
    ax.set_aspect('equal')
    pdf.savefig()
    plt.clf()


def plot_stage_shift_scatter(fig, pdf, X: list, Y: list, U: list, V: list, title: str, *, ymin: float = -5,
                             ymax: float = 5):
    cmap = plt.get_cmap('tab10')
    i = 0
    for (stage, xlabel) in zip([X, Y], ["Stage X [mm]", "Stage Y [mm]"]):
        for (shift, ylabel) in zip([U, V], ["shift_X [um]", "shift_Y [um]"]):
            ax = fig.add_subplot(111, title=title)
            ax.scatter(stage, shift, marker='x', s=1, color=cmap(i))
            ax.set_ylim(ymin, ymax)
            ax.set_xlabel(xlabel)
            ax.set_ylabel(ylabel)
            ax.grid()
            pdf.savefig()
            plt.clf()
            i += 1


basepath = os.getcwd()

path = os.path.join(basepath, 'ValidViewHistory.json')

if not os.path.exists(path):
    sys.exit('there are no file: {}'.format(path))

print('open: {}'.format(path))
with open(path, 'rb') as f:
    vvh = json.load(f)


pdf_path = os.path.join(basepath, '{}_pos.pdf'.format(os.path.basename(basepath)))
print('open to write: {}'.format(pdf_path))
pdf = PdfPages(pdf_path)

index_list = ['X', 'Y', 'Z']

command = [{}, {}]
pos0 = [{}, {}]
pos1 = [{}, {}]

for i in range(2):
    for j in range(len(index_list)):
        command[i][index_list[j]] = []
        pos0[i][index_list[j]] = []
        pos1[i][index_list[j]] = []

for i in range(len(vvh)):
    layer = vvh[i]['ScanLines']['Layer']
    for j in range(len(index_list)):
        command[layer][index_list[j]].append(vvh[i]['ScanLines'][index_list[j]])
        pos0[layer][index_list[j]].append(vvh[i]['Positions0'][index_list[j]])
        pos1[layer][index_list[j]].append(vvh[i]['Positions1'][index_list[j]])

factor = 10000
guide = 0.001
width = 0.5

fig = plt.figure()

# エンコード値 - 指令値のプロット
# Encode Value0がXY駆動直後、Encode Value1が表面認識待ち時間
for i in range(2):
    for num, pos in enumerate([pos0, pos1]):
        title = 'Encode Value{} - Command Value (Layer={})'.format(num, i)
        X = command[i]['X']
        Y = command[i]['Y']
        U = [(x - y) * factor for (x, y) in zip(pos[i]['X'], command[i]['X'])]
        V = [(x - y) * factor for (x, y) in zip(pos[i]['Y'], command[i]['Y'])]
        plot_vec(fig, pdf, X, Y, U, V, title, factor, width=width)

        U = [(x - y) * 1000 for (x, y) in zip(pos[i]['X'], command[i]['X'])]
        V = [(x - y) * 1000 for (x, y) in zip(pos[i]['Y'], command[i]['Y'])]
        plot_stage_shift_scatter(fig, pdf, X, Y, U, V, title, ymin=-1.5, ymax=1.5)

# 上で描画したベクトル量の、L0 - L1の値
for i, pos in enumerate([pos0, pos1]):
    title = 'Layer0 - Layer1 (Encode Value{} - Command Value)'.format(i)
    X = command[0]['X']
    Y = command[0]['Y']
    U = [((ex0 - cx0) - (ex1 - cx1)) * factor for (ex0, cx0, ex1, cx1) in
         zip(pos[0]['X'], command[0]['X'], pos[1]['X'], command[1]['X'])]
    V = [((ey0 - cy0) - (ey1 - cy1)) * factor for (ey0, cy0, ey1, cy1) in
         zip(pos[0]['Y'], command[0]['Y'], pos[1]['Y'], command[1]['Y'])]
    plot_vec(fig, pdf, X, Y, U, V, title, factor, width=width)

    U = [((ex0 - cx0) - (ex1 - cx1)) * 1000 for (ex0, cx0, ex1, cx1) in
         zip(pos[0]['X'], command[0]['X'], pos[1]['X'], command[1]['X'])]
    V = [((ey0 - cy0) - (ey1 - cy1)) * 1000 for (ey0, cy0, ey1, cy1) in
         zip(pos[0]['Y'], command[0]['Y'], pos[1]['Y'], command[1]['Y'])]
    plot_stage_shift_scatter(fig, pdf, X, Y, U, V, title, ymin=-1.5, ymax=1.5)

pdf.close()
