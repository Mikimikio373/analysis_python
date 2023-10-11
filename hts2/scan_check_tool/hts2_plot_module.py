import os
import sys
import math
import copy

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
import itertools

step_x = 9.0
step_y = 4.95

def initial(ValidViewHistry):
    '''

    :param ValidViewHistryのほかにもいるかも?:
    :return: DataFrame['index'][imager id][data*viwe数]
    index一覧:'not_all'....
    '''

def text(array: np.ndarray, ax, color: str):
    for num_r, row in enumerate(array):
        for num_c, value in enumerate(array[num_r]):
            ax.text(num_c, num_r, '{:d}'.format(int(value)), color=color, ha='center', va='center')


def textbox(ax, flat_list, ax_x_max, ax_y_max):
    entries = len(flat_list)
    length = len(str(entries))
    mean = np.mean(flat_list)
    std_dev = np.std(flat_list)
    if len(str(mean)) > length:
        if str(mean)[0:length][-1] == '.':
            str_mean = 'Mean:     {}'.format(str(mean)[0:length - 1])
        else:
            str_mean = 'Mean:    {}'.format(str(mean)[0:length])
    else:
        str_mean = 'Mean:    {}'.format(str(mean).rjust(length))

    if len(str(std_dev)) > length:
        if str(std_dev)[0:length][-1] == '.':
            str_std = 'Std Dev:  {}'.format(str(std_dev)[0:length - 1])
        else:
            str_std = 'Std Dev: {}'.format(str(std_dev)[0:length])
    else:
        str_std = 'Std Dev: {}'.format(str(std_dev).rjust(length))

    text = 'Entries: {}\n{}\n{}'.format(entries, str_mean, str_std)
    ax.text(ax_x_max * 0.9, ax_y_max * 0.9, text, bbox=(dict(boxstyle='square', fc='w')))


def not_all(basepath: str, sensor_pos_sorted, ScanAreaParam, ValidViewHistry, not_max: int):
    """
    スキャンエリアのnot分布を書く関数
    """
    out_path = os.path.join(basepath, 'GRAPH')
    sideX = ScanAreaParam['SideX']
    sideY = ScanAreaParam['SideY']
    layer = ScanAreaParam['Layer']
    step_x_num = math.ceil(sideX / step_x)
    step_y_num = math.ceil(sideY / step_y)
    step_y_num3 = step_y_num * 3
    half_view = step_y_num3 * step_x_num

    # 入れ物用意
    not_l0 = []
    not_l1 = []
    module = 2
    sensor = 12
    for m in range(module):
        for s in range(sensor):
            not_tmp_l0 = []
            not_tmp_l1 = []
            nottxt_path = os.path.join(basepath, 'DATA', '{:02}_{:02}'.format(m, s), 'TrackHit2_0_99999999_0_000.txt')
            if not os.path.exists(nottxt_path):
                sys.exit('there is no file: {}'.format(nottxt_path))

            f = open(nottxt_path, 'r')
            data_line = f.readlines()
            for i in range(len(data_line)):
                # L0, L1の判断 ValidViweHistryを使わなくとも実装できるi % step_x_num*2 < step_x_num
                if ValidViewHistry[i]['Layer'] == 0:  # L0側
                    not_tmp_l0.append([int(data_line[i].split(' ')[-2]), i])
                else:
                    not_tmp_l1.append([int(data_line[i].split(' ')[-2]), i])
            not_l0.append(not_tmp_l0)
            not_l1.append(not_tmp_l1)

    not_array_l0 = np.zeros((step_y_num * 9, step_x_num * 8))
    not_array_l1 = np.zeros((step_y_num * 9, step_x_num * 8))

    print('all scan area view num: {}'.format(half_view))
    print('scaned area view num: {}'.format(len(not_l0[0])))
    for i in range(half_view):
        # 1/3でY方向を3分割しているため何レーン目かを判断
        y_lane = math.floor(i / step_x_num) % 3
        for py in range(9):
            for px in range(8):
                pos = py * 8 + px

                id = sensor_pos_sorted[pos]['id']
                if id > 23:
                    continue
                tmp_l0 = not_l0[id][i]
                tmp_l1 = not_l1[id][i]
                # 全pcolermesh座標系におけるx,yの計算
                array_x_l0 = (i % step_x_num) * 8 + px  # xはviewのx座標とpxで計算
                array_x_l1 = (step_x_num - 1 - (i % step_x_num)) * 8 + px  # l1側はviewの順序を反転
                array_y = math.floor(
                    i / (step_x_num * 3)) * 9 + py + y_lane  # yはstep_x_numの三倍の商がフルセンサーのview_y + ３回のうち何回目か
                not_array_l0[array_y][array_x_l0] = tmp_l0[0]
                not_array_l1[array_y][array_x_l1] = tmp_l1[0]

    cmap = copy.copy(plt.get_cmap("jet"))
    cmap.set_under('w', 1)  # 下限以下の色を設定

    x = np.arange(step_x_num * 8)
    x = x * step_x / 8
    y = np.arange(step_y_num * 9)
    y = y * step_y / 9
    x, y = np.meshgrid(x, y)

    fig = plt.figure(figsize=(11.69, 8.27), tight_layout=True)

    ax1 = plt.subplot(221, title='L0 not')
    z_ber0 = ax1.pcolormesh(x, y, not_array_l0, cmap=cmap, vmin=1, vmax=not_max)
    divider0 = make_axes_locatable(ax1)  # axに紐付いたAxesDividerを取得
    cax0 = divider0.append_axes("right", size="5%", pad=0.1)  # append_axesで新しいaxesを作成
    fig.colorbar(z_ber0, orientation="vertical", cax=cax0)
    ax1.set_aspect('equal')
    ax1.set_xlabel('X [mm]')
    ax1.set_ylabel('Y [mm]')

    ax2 = plt.subplot(222, title='L1 not')
    z_ber1 = ax2.pcolormesh(x, y, not_array_l1, cmap=cmap, vmin=1, vmax=not_max)
    divider1 = make_axes_locatable(ax2)  # axに紐付いたAxesDividerを取得
    cax1 = divider1.append_axes("right", size="5%", pad=0.1)  # append_axesで新しいaxesを作成
    fig.colorbar(z_ber1, orientation="vertical", cax=cax1)
    ax2.set_aspect('equal')
    ax2.set_xlabel('X [mm]')
    ax2.set_ylabel('Y [mm]')

    ax3 = plt.subplot(223, title='L0 not')
    flat_not_l0 = list(itertools.chain.from_iterable(not_array_l0))
    hist_return0 = ax3.hist(flat_not_l0, histtype='step', bins=100, range=(0, not_max), color='w', ec='r')
    textbox(ax3, flat_not_l0, not_max, max(hist_return0[0]))

    ax4 = plt.subplot(224, title='L1 not')
    flat_not_l1 = list(itertools.chain.from_iterable(not_array_l1))
    hist_return1 = ax4.hist(flat_not_l1, histtype='step', bins=100, range=(0, not_max), color='w', ec='b')
    textbox(ax4, flat_not_l1, not_max, max(hist_return1[0]))

    plt.savefig(os.path.join(out_path, 'not_plot.png'), dpi=300)
    print('not_plot.png ended.')