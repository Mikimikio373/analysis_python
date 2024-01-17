import json
import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages


def plot_stage_shift_vec(ax, pdf, X: list, Y: list, U: list, V: list, stage_x: list, stage_y, title: str,
                         factor: float = 10000, *, guide: float = 0.001):
    # 視野のグリッド線を描画
    xw = stage_x[1] - stage_x[0]
    yw = stage_y[1] - stage_y[0]
    for x in stage_x + [max(stage_x) + xw]:
        ax.plot([x - xw / 2, x - xw / 2], [min(stage_y) - yw / 2, max(stage_y) + yw / 2], alpha=0.5, color="tab:orange",
                lw=1)
    for y in stage_y + [max(stage_y) + yw]:
        ax.plot([min(stage_x) - xw / 2, max(stage_x) + xw / 2], [y - yw / 2, y - yw / 2], alpha=0.5, color="tab:orange",
                lw=1)

    # ベクトルマップを描画
    ax.quiver(X, Y, np.asarray(U) * factor, np.asarray(V) * factor, angles='xy', scale_units='xy', scale=1, units='xy',
              width=0.4)

    # 凡例を描画
    x = min(X) - (max(X) - min(X)) * 0.05
    y = min(Y) - (max(Y) - min(Y)) * 0.05
    ax.quiver(x, y, guide * factor, 0, angles='xy', scale_units='xy', scale=1, units='xy', width=0.4)
    ax.quiver(x, y, 0, guide * factor, angles='xy', scale_units='xy', scale=1, units='xy', width=0.4)
    ax.text(x, y, f" {guide * 1000} um", va="bottom", ha="left")

    ax.set_aspect(1)
    ax.set_title(title)
    ax.set_xlabel("Stage X [mm]")
    ax.set_ylabel("Stage Y [mm]")
    pdf.savefig()
    plt.clf()


def plot_stage_shift_scatter(fig, pdf, X: list, Y: list, U: list, V: list, title: str, *, ymin: float = -5,
                             ymax: float = 5):
    cmap = plt.get_cmap('tab10')
    i = 0
    for (stage, xlabel) in zip([X, Y], ["Stage X [mm]", "Stage Y [mm]"]):
        for (shift, ylabel) in zip([U, V], ["shift_X [um]", "shift_Y [um]"]):
            ax = fig.add_subplot(111, title="{} : {} ({})".format(xlabel[0:7], ylabel[0:7], title))
            ax.scatter(stage, shift * 1000, marker='x', s=1, color=cmap(i))
            ax.set_ylim(ymin, ymax)
            ax.yaxis.set_major_locator(mpl.ticker.LinearLocator(11))
            ax.set_xlabel(xlabel)
            ax.set_ylabel(ylabel)
            ax.grid()
            pdf.savefig()
            plt.clf()
            i += 1


def read_ali_stage(path):
    """
    shiftdata[layer]
    flag: 1,X overlap, 2, Y overlap
    :param path:
    :return:
    """
    with open(path, 'rb') as f:
        obj = json.load(f)

    shift_data = [[], []]
    X_tmp = [[], []]
    Y_tmp = [[], []]
    U_tmp = [[], []]
    V_tmp = [[], []]
    flag_tmp = [[], []]
    hit_num_tmp = [[], []]
    stage = [[], []]
    for i in range(2):
        shift_data[i] = pd.DataFrame()
        stage[i] = {}
        stage[i]["stage_x"] = []
        stage[i]["stage_y"] = []
    # データ取得
    for o in obj["ali_stage"]:
        if o["layer"] == 2:
            continue
        flag = 0
        if o["stage_x1"] == o["stage_x2"]:  # yオーバーラップ
            flag = 2
        if o["stage_y1"] == o["stage_y2"]:  # xオーバーラップ
            flag = 1
        sx = (o["stage_x1"] + o["stage_x2"]) * 0.5
        sy = (o["stage_y1"] + o["stage_y2"]) * 0.5
        X_tmp[o["layer"]].append(sx)
        Y_tmp[o["layer"]].append(sy)
        U_tmp[o["layer"]].append(o["shift_x"])
        V_tmp[o["layer"]].append(o["shift_y"])
        flag_tmp[o["layer"]].append(flag)
        hit_num_tmp[o["layer"]].append(o["Nhit"])
        stage[o["layer"]]["stage_x"].append(o["stage_x1"])
        stage[o["layer"]]["stage_x"].append(o["stage_x2"])
        stage[o["layer"]]["stage_y"].append(o["stage_y1"])
        stage[o["layer"]]["stage_y"].append(o["stage_y2"])

    for i in range(2):
        shift_data[i]["X"] = X_tmp[i]
        shift_data[i]["Y"] = Y_tmp[i]
        shift_data[i]["U"] = U_tmp[i]
        shift_data[i]["V"] = V_tmp[i]
        shift_data[i]["flag"] = flag_tmp[i]
        shift_data[i]["hit_num"] = hit_num_tmp[i]

    for i in range(2):
        drop_index = shift_data[i].index[(shift_data[i]['hit_num'] < 100)]
        shift_data[i] = shift_data[i].drop(drop_index)
        shift_data[i] = shift_data[i].reset_index(drop=True)
        shift_data[i] = shift_data[i].sort_values(["X", "Y"])
        shift_data[i] = shift_data[i].reset_index()
        shift_data[i] = shift_data[i].drop("index", axis=1)
    int_df = pd.merge(shift_data[0], shift_data[1], how="inner", on=["X", "Y"])

    return shift_data, int_df, stage

def plot_xydivide(json_path: str, out_pdf_path: str):
    shift_data, int_data, stage = read_ali_stage(json_path)  # データの読み取り
    pdf = PdfPages(out_pdf_path)

    for layer in range(2):
        for (flag, title) in zip([1, 2], ['X overlap', 'Y overlap']):
            X = shift_data[layer].query('flag == {}'.format(flag))['X']
            Y = shift_data[layer].query('flag == {}'.format(flag))['Y']
            U = shift_data[layer].query('flag == {}'.format(flag))['U']
            V = shift_data[layer].query('flag == {}'.format(flag))['V']
            stage_x = sorted(list(set(stage[layer]["stage_x"])))
            stage_y = sorted(list(set(stage[layer]["stage_y"])))

            fig = plt.figure()
            ax = fig.add_subplot(111)

            plot_stage_shift_vec(ax, pdf, X, Y, U, V, stage_x, stage_y, 'layer = {} ({})'.format(layer, title))
            plot_stage_shift_scatter(fig, pdf, X, Y, U, V, 'layer = {} ({})'.format(layer, title))

            plt.clf()

    pdf.close()


def plot_2dif(x: list, dx1: list, dx1_err: list, dx2: list, xlabel: str, ylabel: str, fname: str):
    plt.errorbar(x, dx1, yerr=dx1_err, fmt='x', label='overlap difference')
    plt.plot(x, dx2, 'x', label='total difference')
    plt.xticks(range(0, 251, 25))
    plt.ylim(-12.5, 12.5)
    plt.yticks(range(-12, 13, 2))
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.grid()
    plt.legend()
    plt.savefig(fname, dpi=300)
    plt.clf()
    plt.close()
