import os
import sys
import math
import copy
import json

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
import itertools

step_x = 9.0
step_y = 5.0
index_list1 = ['excount', 'nog_all', 'nog_over_thr', 'start_picnum', 'nog0', 'nog15', 'top2bottom',
               'top5brightness', 'loop1', 'filter1', 'trackingtime', 'fine_z', 'not']
index_list2 = ['ThickOfLayer', 'repeatTime', 'drivingX', 'drivingY', 'drivingZ', 'DrivingTimePiezo', 'DampingTime',
               'DrivingTimeAll']


def read_not(basepath: str, module: int = 6, sensor: int = 12):
    """

    :param basepath: スキャンデータのbasepath
    :param module: module数, defaultは6
    :param sensor: 1module内でのsensor数, defaultは12
    :return: 1:txtのデータをreadlinesでimagerごとに配列にしたもの, 2:rlクラスタリングがある場合はTrue
    """
    with open(os.path.join(basepath, 'ScanControllParam.json'), 'rb') as f:
        scan_cont_json = json.load(f)

    rl_mode = 'ClusterRadialParam' in scan_cont_json['TrackingParam']['CommonParamArray'][0]
    txt_data = []
    for m in range(module):
        for s in range(sensor):
            nottxt_path = os.path.join(basepath, 'DATA', '{:02}_{:02}'.format(m, s),
                                       'TrackHit2_0_99999999_0_000.txt')
            if not os.path.exists(nottxt_path):
                sys.exit('there is no file: {}'.format(nottxt_path))

            f = open(nottxt_path, 'r')
            data_line = f.readlines()
            txt_data.append(data_line)

    return txt_data, rl_mode


def initial(vvh_json: dict, sap_json: dict, basepath: str, mode: int = 0):
    """

    :param vvh_json: ValidViewHistryのjsonデータ
    :param sap_json: ScanAreaParamのjsonデータ
    :param basepath: スキャンの出力フォルダ
    :param mode: 0:フルセンサー, 1:1/3モード
    :return: 1:センサーごとのDataFrame['index'][layer][imager id][data*view数], 2:センサーに依存しないDataFrame['index'][view数]

    out1 index一覧:'excount', 'nog_all', 'nog_over_thr', 'start_picnum', 'nog0', 'nog15', 'top2bottom', 'top5brightness', 'fine_z', 'loop1', 'filter1', 'trackingtime', 'not'

    out2 index一覧:'ThickOfLayer', 'repeatTime', 'drivingX', 'drivingY', 'drivingZ', 'DrivingTimePiezo', 'DampingTime', 'DrivingTimeAll'
    """
    global index_list1, index_list2

    print('Initial')
    print('scanned view num: {}'.format(len(vvh_json)))
    module = 6
    sensor = 12
    if mode == 1:
        module = 2
        sensor = 12
    else:
        print('未対応modeです')
        sys.exit()
    imager_num = module * sensor
    layer = sap_json['Layer']
    not_txtdata, rl_mode = read_not(basepath, module=module, sensor=sensor)

    tmp_list1 = []
    tmp_list2 = []
    for i in range(layer):
        tmp_list1.append([])
        tmp_list2.append([])
    for i in range(layer):
        for j in range(imager_num):
            tmp_list1[i].append([])
    out1 = {}
    out2 = {}
    for i in range(len(index_list1)):
        out1[index_list1[i]] = copy.deepcopy(tmp_list1)
    for i in range(len(index_list2)):
        out2[index_list2[i]] = copy.deepcopy(tmp_list2)

    for view in range(len(vvh_json)):
        L = int(vvh_json[view]['Layer'])
        thickness = vvh_json[view]['ScanEachLayerParam']['ThickOfLayer']
        Npicthickness = vvh_json[view]['ScanEachLayerParam']['NPicThickOfLayer']
        out2[index_list2[0]][L].append(thickness)  # ThickOfLayer
        out2[index_list2[1]][L].append(vvh_json[view]['RepeatTimes'])  # repeatTime
        out2[index_list2[2]][L].append(vvh_json[view]['DrivingTimeXYZ'][0])  # dirivingX
        out2[index_list2[3]][L].append(vvh_json[view]['DrivingTimeXYZ'][1])  # dirivingY
        out2[index_list2[4]][L].append(vvh_json[view]['DrivingTimeXYZ'][2])  # dirivingZ
        out2[index_list2[5]][L].append(vvh_json[view]['DrivingTimePiezo'])  # DrivingTimePiezo
        out2[index_list2[6]][L].append(vvh_json[view]['DampingTime'])  # DampingTime
        out2[index_list2[7]][L].append(vvh_json[view]['DrivingTimeAll'])  # DrivingTime

        for id in range(imager_num):
            StartPicNum = vvh_json[view]['StartAnalysisPicNo'][id]
            EndPicNum = StartPicNum + 15
            out1[index_list1[0]][L][id].append(vvh_json[view]['ImagerControllerParam']['ExposureCount'][id])  # excount
            out1[index_list1[1]][L][id].append(vvh_json[view]['Nogs'][id])  # nog all
            out1[index_list1[2]][L][id].append(vvh_json[view]['SurfaceDetail'][id]['NogOverThr'])  # nog_over_thr
            out1[index_list1[3]][L][id].append(StartPicNum)  # StartPicNum
            out1[index_list1[4]][L][id].append(vvh_json[view]['Nogs'][id][StartPicNum])  # nog0
            out1[index_list1[5]][L][id].append(vvh_json[view]['Nogs'][id][EndPicNum])  # nog15
            out1[index_list1[6]][L][id].append(
                vvh_json[view]['SurfaceDetail'][id]['Bottom'] - vvh_json[view]['SurfaceDetail'][id][
                    'Top'])  # top2bottom
            out1[index_list1[7]][L][id].append(
                vvh_json[view]['ImagerControllerParam']['Top5Brightness'][id])  # top5brightness
            out1[index_list1[8]][L][id].append(vvh_json[view]['ProcessTimeLoop1'][id])  # loop1
            out1[index_list1[9]][L][id].append(vvh_json[view]['ProcessTimeImageFilter1'][id])  # filter1
            out1[index_list1[10]][L][id].append(vvh_json[view]['ProcessTimeTracking1'][id])  # trackingtime
            # fine_z
            if L == 0:
                fine_z = vvh_json[view]['ScanLines']['Z'] * 1000 + (thickness / Npicthickness * EndPicNum)
            else:
                fine_z = vvh_json[view]['ScanLines']['Z'] * 1000 + (thickness / Npicthickness * StartPicNum)
            out1[index_list1[11]][L][id].append(fine_z)
            # not
            if rl_mode:
                out1[index_list1[12]][L][id].append(int(not_txtdata[id][view].split(' ')[-3]))
            else:
                out1[index_list1[12]][L][id].append(int(not_txtdata[id][view].split(' ')[-2]))

    return out1, out2


def text(array: np.ndarray, ax, color: str):
    for num_r, row in enumerate(array):
        for num_c, value in enumerate(array[num_r]):
            ax.text(num_c, num_r, '{:g}'.format(value), color=color, ha='center', va='center')


def textbox(ax, flat_list, ax_x_max, ax_y_max, *, factor: float = 0.9):
    entries = len(flat_list)
    mean = np.mean(flat_list)
    std_dev = np.std(flat_list)

    text = 'Entries: {:d}\nMean: {:4g}\nStd_dev: {:4g}'.format(entries, mean, std_dev)
    ax.text(ax_x_max * factor, ax_y_max * factor, text, bbox=(dict(boxstyle='square', fc='w')))


def plot_area(input_data: list, zmin: float, zmax: float, step_x_num: int, step_y_num: int, title: str,
              sensor_pos_sorted: dict or list, out_file: str, *, bins: int = 100):
    cmap = copy.copy(plt.get_cmap("jet"))
    cmap.set_under('w', 0.0001)  # 下限以下の色を設定

    plot_array = [[], []]
    plot_array[0] = np.zeros((step_y_num * 9, step_x_num * 8))
    plot_array[1] = np.zeros((step_y_num * 9, step_x_num * 8))
    if zmax - zmin < float(bins):
        bins = int(zmax - zmin)

    scaned_ara_view = step_x_num * step_y_num * 3  # step数から計算。1/3モードのため、view数は3倍

    for i in range(scaned_ara_view):
        # 1/3でY方向を3分割しているため何レーン目かを判断
        y_lane = math.floor(i / step_x_num) % 3
        for py in range(9):
            for px in range(8):
                pos = py * 8 + px
                id = sensor_pos_sorted[pos]['id']
                if id > 23:
                    continue
                tmp_l0 = input_data[0][id][i]
                tmp_l1 = input_data[1][id][i]
                # 全pcolermesh座標系におけるx,yの計算
                array_x_l0 = (i % step_x_num) * 8 + px  # xはviewのx座標とpxで計算
                array_x_l1 = (step_x_num - 1 - (i % step_x_num)) * 8 + px  # l1側はviewの順序を反転
                array_y = math.floor(
                    i / (step_x_num * 3)) * 9 + py + y_lane  # yはstep_x_numの三倍の商がフルセンサーのview_y + ３回のうち何回目か
                plot_array[0][array_y][array_x_l0] = tmp_l0
                plot_array[1][array_y][array_x_l1] = tmp_l1

    x = np.arange(step_x_num * 8)
    x = x * step_x / 8
    y = np.arange(step_y_num * 9)
    y = y * step_y / 9
    x, y = np.meshgrid(x, y)

    fig = plt.figure(figsize=(11.69, 8.27), tight_layout=True)
    fig.suptitle(title, fontsize=20)
    ax1 = plt.subplot(221, title='Layer0')
    z_ber0 = ax1.pcolormesh(x, y, plot_array[0], cmap=cmap, vmin=zmin, vmax=zmax)
    divider0 = make_axes_locatable(ax1)  # axに紐付いたAxesDividerを取得
    cax0 = divider0.append_axes("right", size="5%", pad=0.1)  # append_axesで新しいaxesを作成
    pp0 = fig.colorbar(z_ber0, orientation="vertical", cax=cax0)
    ax1.set_aspect('equal')
    ax1.set_xlabel('X [mm]')
    ax1.set_ylabel('Y [mm]')

    ax2 = plt.subplot(222, title='Layer1')
    z_ber1 = ax2.pcolormesh(x, y, plot_array[1], cmap=cmap, vmin=zmin, vmax=zmax)
    divider1 = make_axes_locatable(ax2)  # axに紐付いたAxesDividerを取得
    cax1 = divider1.append_axes("right", size="5%", pad=0.1)  # append_axesで新しいaxesを作成
    pp1 = fig.colorbar(z_ber1, orientation="vertical", cax=cax1)
    ax2.set_aspect('equal')
    ax2.set_xlabel('X [mm]')
    ax2.set_ylabel('Y [mm]')

    ax3 = plt.subplot(223, title='Layer0')
    flat_data_l0 = list(itertools.chain.from_iterable(plot_array[0]))
    hist_return0 = ax3.hist(flat_data_l0, histtype='step', bins=bins, range=(zmin, zmax), color='w', ec='r')
    textbox(ax3, flat_data_l0, zmax, max(hist_return0[0]))

    ax4 = plt.subplot(224, title='Layer1')
    flat_data_l1 = list(itertools.chain.from_iterable(plot_array[1]))
    hist_return1 = ax4.hist(flat_data_l1, histtype='step', bins=bins, range=(zmin, zmax), color='w', ec='b')
    textbox(ax4, flat_data_l1, zmax, max(hist_return1[0]))

    plt.savefig(out_file, dpi=300)
    print('{} written'.format(out_file))


def plot_area_view(input_data: list, zmin: float, zmax: float, step_x_num: int, step_y_num: int, title: str,
                   sensor_pos_sorted: dict or list, out_file: str, *, bins: int = 100):
    cmap = copy.copy(plt.get_cmap("jet"))
    cmap.set_under('w', 0.0001)  # 下限以下の色を設定

    plot_array = [[], []]
    plot_array[0] = np.zeros((step_y_num * 9, step_x_num * 8))
    plot_array[1] = np.zeros((step_y_num * 9, step_x_num * 8))

    scaned_ara_view = step_x_num * step_y_num * 3  # step数から計算。1/3モードのため、view数は3倍

    for i in range(scaned_ara_view):
        # 1/3でY方向を3分割しているため何レーン目かを判断
        y_lane = math.floor(i / step_x_num) % 3
        for py in range(9):
            for px in range(8):
                pos = py * 8 + px
                id = sensor_pos_sorted[pos]['id']
                if id > 23:
                    continue
                tmp_l0 = input_data[0][i]
                tmp_l1 = input_data[1][i]
                # 全pcolermesh座標系におけるx,yの計算
                array_x_l0 = (i % step_x_num) * 8 + px  # xはviewのx座標とpxで計算
                array_x_l1 = (step_x_num - 1 - (i % step_x_num)) * 8 + px  # l1側はviewの順序を反転
                array_y = math.floor(
                    i / (step_x_num * 3)) * 9 + py + y_lane  # yはstep_x_numの三倍の商がフルセンサーのview_y + ３回のうち何回目か
                plot_array[0][array_y][array_x_l0] = tmp_l0
                plot_array[1][array_y][array_x_l1] = tmp_l1

    x = np.arange(step_x_num * 8)
    x = x * step_x / 8
    y = np.arange(step_y_num * 9)
    y = y * step_y / 9
    x, y = np.meshgrid(x, y)

    fig = plt.figure(figsize=(11.69, 8.27), tight_layout=True)
    fig.suptitle(title, fontsize=20)
    ax1 = plt.subplot(221, title='Layer0')
    z_ber0 = ax1.pcolormesh(x, y, plot_array[0], cmap=cmap, vmin=zmin, vmax=zmax)
    divider0 = make_axes_locatable(ax1)  # axに紐付いたAxesDividerを取得
    cax0 = divider0.append_axes("right", size="5%", pad=0.1)  # append_axesで新しいaxesを作成
    pp0 = fig.colorbar(z_ber0, orientation="vertical", cax=cax0)
    ax1.set_aspect('equal')
    ax1.set_xlabel('X [mm]')
    ax1.set_ylabel('Y [mm]')

    ax2 = plt.subplot(222, title='Layer1')
    z_ber1 = ax2.pcolormesh(x, y, plot_array[1], cmap=cmap, vmin=zmin, vmax=zmax)
    divider1 = make_axes_locatable(ax2)  # axに紐付いたAxesDividerを取得
    cax1 = divider1.append_axes("right", size="5%", pad=0.1)  # append_axesで新しいaxesを作成
    pp1 = fig.colorbar(z_ber1, orientation="vertical", cax=cax1)
    ax2.set_aspect('equal')
    ax2.set_xlabel('X [mm]')
    ax2.set_ylabel('Y [mm]')

    ax3 = plt.subplot(223, title='Layer0')
    flat_data_l0 = list(itertools.chain.from_iterable(plot_array[0]))
    hist_return0 = ax3.hist(flat_data_l0, histtype='step', bins=bins, range=(zmin, zmax), color='w', ec='r')
    textbox(ax3, flat_data_l0, zmax, max(hist_return0[0]))

    ax4 = plt.subplot(224, title='Layer1')
    flat_data_l1 = list(itertools.chain.from_iterable(plot_array[1]))
    hist_return1 = ax4.hist(flat_data_l1, histtype='step', bins=bins, range=(zmin, zmax), color='w', ec='b')
    textbox(ax4, flat_data_l1, zmax, max(hist_return1[0]))

    plt.savefig(out_file, dpi=300)
    print('{} written'.format(out_file))


def plot_finez(input_data: list, zmin: float, zmax: float, basemin: float, basemax: float, step_x_num: int,
               step_y_num: int, title: str, sensor_pos_sorted: dict or list, out_file: str, *, bins: int = 100,
               basebins: int = 100):
    cmap = copy.copy(plt.get_cmap("jet"))
    cmap.set_under('w', 0.0001)  # 下限以下の色を設定

    plot_array = [[], []]
    plot_array[0] = np.zeros((step_y_num * 9, step_x_num * 8))
    plot_array[1] = np.zeros((step_y_num * 9, step_x_num * 8))
    if zmax - zmin < float(bins):
        bins = int(zmax - zmin)

    scaned_ara_view = step_x_num * step_y_num * 3  # step数から計算。1/3モードのため、view数は3倍

    for i in range(scaned_ara_view):
        # 1/3でY方向を3分割しているため何レーン目かを判断
        y_lane = math.floor(i / step_x_num) % 3
        for py in range(9):
            for px in range(8):
                pos = py * 8 + px
                id = sensor_pos_sorted[pos]['id']
                if id > 23:
                    continue
                tmp_l0 = input_data[0][id][i]
                tmp_l1 = input_data[1][id][i]
                # 全pcolermesh座標系におけるx,yの計算
                array_x_l0 = (i % step_x_num) * 8 + px  # xはviewのx座標とpxで計算
                array_x_l1 = (step_x_num - 1 - (i % step_x_num)) * 8 + px  # l1側はviewの順序を反転
                array_y = math.floor(
                    i / (step_x_num * 3)) * 9 + py + y_lane  # yはstep_x_numの三倍の商がフルセンサーのview_y + ３回のうち何回目か
                plot_array[0][array_y][array_x_l0] = tmp_l0
                plot_array[1][array_y][array_x_l1] = tmp_l1

    x = np.arange(step_x_num * 8)
    x = x * step_x / 8
    y = np.arange(step_y_num * 9)
    y = y * step_y / 9
    x, y = np.meshgrid(x, y)

    fig = plt.figure(figsize=(8.27 * 1.5, 11.69 * 1.5), tight_layout=True)
    fig.suptitle(title, fontsize=20)
    ax1 = plt.subplot(321, title='Layer0')
    z_ber0 = ax1.pcolormesh(x, y, plot_array[0], cmap=cmap, vmin=zmin, vmax=zmax)
    divider0 = make_axes_locatable(ax1)  # axに紐付いたAxesDividerを取得
    cax0 = divider0.append_axes("right", size="5%", pad=0.1)  # append_axesで新しいaxesを作成
    pp0 = fig.colorbar(z_ber0, orientation="vertical", cax=cax0)
    ax1.set_aspect('equal')
    ax1.set_xlabel('X [mm]')
    ax1.set_ylabel('Y [mm]')

    ax2 = plt.subplot(322, title='Layer1')
    z_ber1 = ax2.pcolormesh(x, y, plot_array[1], cmap=cmap, vmin=zmin, vmax=zmax)
    divider1 = make_axes_locatable(ax2)  # axに紐付いたAxesDividerを取得
    cax1 = divider1.append_axes("right", size="5%", pad=0.1)  # append_axesで新しいaxesを作成
    pp1 = fig.colorbar(z_ber1, orientation="vertical", cax=cax1)
    ax2.set_aspect('equal')
    ax2.set_xlabel('X [mm]')
    ax2.set_ylabel('Y [mm]')

    ax3 = plt.subplot(323, title='Layer0')
    flat_data_l0 = list(itertools.chain.from_iterable(plot_array[0]))
    hist_return0 = ax3.hist(flat_data_l0, histtype='step', bins=bins, range=(zmin, zmax), color='w', ec='r')
    ax3.set_xlabel('Z0 [um]')
    textbox(ax3, flat_data_l0, zmax, max(hist_return0[0]), factor=0.99)

    ax4 = plt.subplot(324, title='Layer1')
    flat_data_l1 = list(itertools.chain.from_iterable(plot_array[1]))
    hist_return1 = ax4.hist(flat_data_l1, histtype='step', bins=bins, range=(zmin, zmax), color='w', ec='b')
    ax4.set_xlabel('Z1 [um]')
    textbox(ax4, flat_data_l1, zmax, max(hist_return1[0]), factor=0.99)

    ax5 = plt.subplot(325, title='Thickness of Base (2D)')
    z_ber3 = ax5.pcolormesh(x, y, plot_array[1] - plot_array[0], cmap=cmap, vmin=basemin, vmax=basemax)
    divider3 = make_axes_locatable(ax5)  # axに紐付いたAxesDividerを取得
    cax3 = divider3.append_axes("right", size="5%", pad=0.1)  # append_axesで新しいaxesを作成
    pp3 = fig.colorbar(z_ber3, orientation="vertical", cax=cax3)
    ax5.set_aspect('equal')
    ax5.set_xlabel('X [mm]')
    ax5.set_ylabel('Y [mm]')

    ax6 = plt.subplot(326, title='Thickness of Base')
    flat_data_base = list(itertools.chain.from_iterable(plot_array[1] - plot_array[0]))
    hist_return2 = ax6.hist(flat_data_base, histtype='step', bins=bins, range=(basemin, basemax), color='w', ec='r')
    ax6.set_xlabel('base [um]')
    textbox(ax6, flat_data_base, basemax, max(hist_return2[0]), factor=0.95)

    plt.savefig(out_file, dpi=300)
    print('{} written'.format(out_file))


def plot_sensor(input_data: list, zmin: float, zmax: float, title: str,
                sensor_pos_sorted: dict or list, out_file: str):
    average_data = [[], []]
    for i in range(len(input_data[0])):
        for L in range(2):
            average_data[L].append(np.average(input_data[L][i]))

    cmap = copy.copy(plt.get_cmap("jet"))
    cmap.set_under('w', 0.0001)  # 下限以下の色を設定
    x = np.arange(8)
    y = np.arange(9)
    x, y = np.meshgrid(x, y)
    z = [[], []]
    for L in range(2):
        z[L] = np.zeros((9, 8))

    for py in range(9):
        for px in range(8):
            id = sensor_pos_sorted[py * 8 + px]['id']
            for L in range(2):
                if id > 23:
                    z[L][py][px] = 0
                else:
                    z[L][py][px] = average_data[L][id]

    fig = plt.figure(figsize=(11.69, 8.27), tight_layout=True)
    fig.suptitle(title, fontsize=20)
    ax0 = plt.subplot(221, title='Layer0 array')
    z_ber0 = ax0.pcolormesh(x, y, z[0], cmap=cmap, vmin=zmin, vmax=zmax, edgecolors="black")
    text(z[0], ax0, 'black')
    divider0 = make_axes_locatable(ax0)  # axに紐付いたAxesDividerを取得
    cax0 = divider0.append_axes("right", size="5%", pad=0.1)  # append_axesで新しいaxesを作成
    pp0 = fig.colorbar(z_ber0, orientation="vertical", cax=cax0)

    ax1 = plt.subplot(222, title='Layer1 array')
    z_ber1 = ax1.pcolormesh(x, y, z[1], cmap=cmap, vmin=zmin, vmax=zmax, edgecolors="black")
    text(z[1], ax1, 'black')
    divider1 = make_axes_locatable(ax1)  # axに紐付いたAxesDividerを取得
    cax1 = divider1.append_axes("right", size="5%", pad=0.1)  # append_axesで新しいaxesを作成
    pp1 = fig.colorbar(z_ber1, orientation="vertical", cax=cax1)

    ax2 = plt.subplot(223, title='Layer0')
    x = np.arange(24)
    ax2.plot(x, average_data[0], marker='x', c='r')
    ax2.set_ylim(zmin, zmax)
    ax2.set_xticks(x)
    ax2.grid()

    ax3 = plt.subplot(224, title='Layer1')
    x = np.arange(24)
    ax3.plot(x, average_data[1], marker='x', c='b')
    ax3.set_ylim(zmin, zmax)
    ax3.set_xticks(x)
    ax3.grid()

    plt.savefig(out_file, dpi=300)
    print('{} written'.format(out_file))

def plot_sensor_not(input_data: list, title: str,
                sensor_pos_sorted: dict or list, out_file: str, *, relative_min: float = 0.8, absolute_max: float = 30000):

    average_data = [[], []]
    for i in range(len(input_data[0])):
        for L in range(2):
            average_data[L].append(np.average(input_data[L][i]))

    cmap = copy.copy(plt.get_cmap("jet"))
    cmap.set_under('w', 0.0001)  # 下限以下の色を設定
    x = np.arange(8)
    y = np.arange(9)
    x, y = np.meshgrid(x, y)
    not_max = [max(average_data[0]), max(average_data[1])]
    z = [[], []]
    for L in range(2):
        z[L] = np.zeros((9, 8))

    for py in range(9):
        for px in range(8):
            id = sensor_pos_sorted[py * 8 + px]['id']
            for L in range(2):
                if id > 23:
                    z[L][py][px] = 0
                else:
                    z[L][py][px] = average_data[L][id] / not_max[L]

    fig = plt.figure(figsize=(8.27 * 1.5, 11.69 * 1.5), tight_layout=True)
    fig.suptitle('Number Of Tracks', fontsize=20)
    x = np.arange(24)
    ax1 = fig.add_subplot(321)
    ax1.plot(x, average_data[0], marker='x', c='r')
    ax1.set_title('Layer0 (absolute)')
    ax1.set_xticks(x)
    ax1.set_xlabel('Imager ID')
    ax1.set_ylim(1, absolute_max)
    ax1.grid()

    ax2 = fig.add_subplot(322)
    ax2.plot(x, average_data[1], marker='x', c='b')
    ax2.set_title('Layer1 (absolute)')
    ax2.set_xticks(x)
    ax2.set_xlabel('Imager ID')
    ax2.set_ylim(1, absolute_max)
    ax2.grid()

    x = np.arange(8)
    y = np.arange(9)
    x, y = np.meshgrid(x, y)
    ax3 = plt.subplot(323, title='Layer0  (relative, sensor array)')
    z_ber0 = ax3.pcolormesh(x, y, z[0], cmap=cmap, vmax=1, vmin=0.8, edgecolors="black")
    divider0 = make_axes_locatable(ax3)  # axに紐付いたAxesDividerを取得
    cax0 = divider0.append_axes("right", size="5%", pad=0.1)  # append_axesで新しいaxesを作成
    text(z[0], ax3, 'black')
    pp0 = fig.colorbar(z_ber0, orientation="vertical", cax=cax0)

    ax4 = plt.subplot(324, title='Layer1 (relative, sensor array)')
    z_ber1 = ax4.pcolormesh(x, y, z[1], cmap=cmap, vmax=1, vmin=relative_min, edgecolors="black")
    divider1 = make_axes_locatable(ax4)  # axに紐付いたAxesDividerを取得
    cax1 = divider1.append_axes("right", size="5%", pad=0.1)  # append_axesで新しいaxesを作成
    text(z[1], ax4, 'black')
    pp1 = fig.colorbar(z_ber1, orientation="vertical", cax=cax1)

    average_data_relative = [[], []]
    average_data_relative[0] = np.asarray(average_data[0]) / not_max[0]
    average_data_relative[1] = np.asarray(average_data[1]) / not_max[1]
    x = np.arange(24)
    ax5 = fig.add_subplot(325)
    ax5.plot(x, average_data_relative[0], marker='x', c='r', label='Layer0 (relative)')
    ax5.plot(x, average_data_relative[1], marker='x', c='b', label='Layer1 (relative)')
    ax5.set_title('NOT (relative)')
    ax5.set_xticks(x)
    ax5.set_xlabel('Imager ID')
    ax5.set_ylim(relative_min, 1)
    ax5.legend()
    ax5.grid()

    plt.savefig(os.path.join(out_file), dpi=300)
    print('{} written'.format(out_file))
