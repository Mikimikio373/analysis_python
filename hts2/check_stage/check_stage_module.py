import json
import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt


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


def plot_stage_shift_scatter(fig, pdf, X: list, Y: list, U: list, V: list, layer: str, *, ymin: float = -5,
                             ymax: float = 5):
    cmap = plt.get_cmap('tab10')
    i = 0
    for (stage, xlabel) in zip([X, Y], ["Stage X [mm]", "Stage Y [mm]"]):
        for (shift, ylabel) in zip([U, V], ["shift_X [um]", "shift_Y [um]"]):
            ax = fig.add_subplot(111, title="{} : {} (Layer = {})".format(xlabel[0:7], ylabel[0:7], layer))
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
    with open('ali.json', 'rb') as f:
        obj = json.load(f)

    shift_data = [[], []]
    X_tmp = [[], []]
    Y_tmp = [[], []]
    U_tmp = [[], []]
    V_tmp = [[], []]
    flag_tmp = [[], []]
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

    for i in range(2):
        shift_data[i] = shift_data[i].sort_values(["X", "Y"])
        shift_data[i] = shift_data[i].reset_index()
        shift_data[i] = shift_data[i].drop("index", axis=1)
    int_df = pd.merge(shift_data[0], shift_data[1], how="inner", on=["X", "Y"])

    return shift_data, int_df, stage

