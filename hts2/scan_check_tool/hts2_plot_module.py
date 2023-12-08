import os
import sys
import math
import copy
import shutil

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
import itertools
from argparse import ArgumentParser

step_x = 9.0
step_y = 5.0
index_list1 = ['excount', 'nog_all', 'nog_over_thr', 'start_picnum', 'nog0', 'nog15', 'top2bottom',
               'top5brightness', 'loop1', 'filter1', 'trackingtime', 'fine_z', 'not', 'main_process', 'not_uncrust']
index_list2 = ['ThickOfLayer', 'repeatTime', 'surf_judge']

index_list3 = ['repeatTime', 'drivingX', 'drivingY', 'drivingZ', 'DrivingTimePiezo', 'DampingTime',
               'DrivingTimeAll', 'ElapsedTime']


def get_option() -> ArgumentParser.parse_args:
    argparser = ArgumentParser()
    argparser.add_argument('-ex', '--exposure_range', nargs=2,
                           type=float,
                           default=[0.1, 1000],
                           metavar=('min', 'max'),
                           help='Range of exposure count. default=[0.1, 1000]')
    argparser.add_argument('-nog', '--nog_range', nargs=2,
                           type=float,
                           default=[0.1, 60000],
                           metavar=('min', 'max'),
                           help='Range of NOG. default=[0.1, 60000]')
    argparser.add_argument('-nog0', '--nog0_range', nargs=2,
                           type=float,
                           default=[0.1, 100000],
                           metavar=('min', 'max'),
                           help='Range of NOG0. default=[0.1, 100000]')
    argparser.add_argument('-nog15', '--nog15_range', nargs=2,
                           type=float,
                           default=[0.1, 100000],
                           metavar=('min', 'max'),
                           help='Range of NOG15. default=[0.1, 100000]')
    argparser.add_argument('-not', '--not_absolute_max', type=float,
                           default=30000,
                           metavar='max',
                           help='Maximum of not (absolute). default=30000')
    argparser.add_argument('-not_un', '--unclusst_not_max', type=float,
                           default=1000000,
                           metavar='max',
                           help='Maximum of not (absolute). default=1000000')
    argparser.add_argument('-process', '--main_process_max', type=float,
                           default=400,
                           metavar='max',
                           help='Maximum of not (absolute). default=400')
    argparser.add_argument('-notrmin', '--not_relative_min', type=float,
                           default=0.7,
                           metavar='min',
                           help='Minimum of not (relative). default=0.7')
    argparser.add_argument('-bs', '--base_surface_range', nargs=4,
                           type=float,
                           default=[11100, 11700, 11300, 11900],
                           metavar=('L0 min', 'L0 max', 'L1 min', 'L1 max'),
                           help='Range of base surface. default=[11100, 11700, 11300, 11900]')
    argparser.add_argument('-bt', '--base_thickness_range', nargs=2,
                           type=float,
                           default=[180, 240],
                           metavar=('min', 'max'),
                           help='Range of base thickness. default=[180, 240]')
    argparser.add_argument('-id', '--imager_id', type=int,
                           default=18,
                           metavar='Imager ID',
                           help='Number of Imager ID. default=18')
    argparser.add_argument('-noga', '--nog_all_max', type=int,
                           default=80000,
                           metavar='max',
                           help='Maximum of nog all. default=80000')
    argparser.add_argument('-on', '--only_plot', nargs='+',
                           type=str,
                           choices=['ex', 'nog', 'nog0', 'nog15', 'toptobottom', 'not', 'not_un', 'mainprocess', 'startpicnum', 'thickoflayer',
                                    'base', 'freq', 'bright', 'nog_all', 'text'],
                           default=[],
                           metavar='Names',
                           help='plot only given arguments: [ex, nog, nog0, nog15, toptobottom, not, not_un, mainprocess, startpicnum'
                                ', thickoflayer, base, freq, bright, nog_all, text]')
    argparser.add_argument('-off', '--off_plot', nargs='+',
                           type=str,
                           choices=['ex', 'nog', 'nog0', 'nog15', 'toptobottom', 'not', 'not_un', 'mainprocess', 'startpicnum', 'thickoflayer',
                                    'base', 'freq', 'bright', 'nog_all', 'text'],
                           default=[],
                           metavar='Names',
                           help='plot only given arguments: [ex, nog, nog0, nog15, toptobottom, not, not_un, mainprocess, startpicnum'
                                ', thickoflayer, base, freq, bright, nog_all, text]')
    return argparser.parse_args()


def copy_notdata(basepath: str, not_path: str, mode):
    if mode == 0:
        module = 6
        sensor = 12
    elif mode == 1:
        module = 2
        sensor = 12
    else:
        module = None
        sensor = None
    for m in range(module):
        for s in range(sensor):
            target_txt = os.path.join(basepath, 'DATA', '{:02}_{:02}'.format(m, s), 'TrackHit2_0_99999999_0_000.txt')
            target_json = os.path.join(basepath, 'DATA', '{:02}_{:02}'.format(m, s), 'TrackHit2_0_99999999_0_000.json')
            if not os.path.exists(target_txt):
                print('There is no file: {}'.format(target_txt))
                continue
            if not os.path.exists(target_json):
                print('There is no file: {}'.format(target_json))
                continue

            shutil.copy2(target_txt, os.path.join(not_path, '{:02}_{:02}_TrackHit2_0_99999999_0_000.txt'.format(m, s)))
            shutil.copy2(target_json,
                         os.path.join(not_path, '{:02}_{:02}_TrackHit2_0_99999999_0_000.json'.format(m, s)))


def read_not(not_path: str, module: int = 6, sensor: int = 12):
    """

    :param not_path: スキャンデータのbasepath
    :param module: module数, defaultは6
    :param sensor: 1module内でのsensor数, defaultは12
    :return: 1:txtのデータをreadlinesでimagerごとに配列にしたもの, 2:rlクラスタリングがある場合はTrue
    """

    txt_data = []
    for m in range(module):
        for s in range(sensor):
            nottxt_path = os.path.join(not_path, '{:02}_{:02}_TrackHit2_0_99999999_0_000.txt'.format(m, s))
            if not os.path.exists(nottxt_path):
                sys.exit('there is no file: {}'.format(nottxt_path))

            f = open(nottxt_path, 'r')
            data_line = f.readlines()
            txt_data.append(data_line)

    return txt_data


def initial(vvh_json: dict, not_path: str, layer: int = 2, mode: int = 0):
    """

    :param vvh_json: ValidViewHistryのjsonデータ
    :param not_path: not dataの出力先path
    :param layer: スキャン時のlayer数
    :param mode: 0:フルセンサー, 1:1/3モード
    :return: 1:センサーごとのdict['index'][layer][imager id][data*view数], 2:センサーに依存しないdict['index'][layer][view数], 3:センサーにもlayerにも依存しないdict['index'][view数]

    out1 index一覧:'excount', 'nog_all', 'nog_over_thr', 'start_picnum', 'nog0', 'nog15', 'top2bottom', 'top5brightness',
     'fine_z', 'loop1', 'filter1', 'trackingtime', 'not', 'main_process', 'not_uncrust'

    out2 index一覧:'ThickOfLayer', 'repeatTime', 'surf_judge'

    out3 index一覧:'repeatTime', 'drivingX', 'drivingY', 'drivingZ', 'DrivingTimePiezo', 'DampingTime', 'DrivingTimeAll',
     'ElapsedTime'
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
    not_txtdata = read_not(not_path, module=module, sensor=sensor)

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
    out3 = {}
    for i in range(len(index_list1)):
        out1[index_list1[i]] = copy.deepcopy(tmp_list1)
    for i in range(len(index_list2)):
        out2[index_list2[i]] = copy.deepcopy(tmp_list2)
    for i in range(len(index_list3)):
        out3[index_list3[i]] = []

    for view in range(len(vvh_json)):
        L = int(vvh_json[view]['Layer'])
        thickness = vvh_json[view]['ScanEachLayerParam']['ThickOfLayer']
        Npicthickness = vvh_json[view]['ScanEachLayerParam']['NPicThickOfLayer']
        out2[index_list2[0]][L].append(thickness)  # ThickOfLayer
        out2[index_list2[1]][L].append(vvh_json[view]['RepeatTimes'])  # repeatTime
        out2[index_list2[2]][L].append(vvh_json[view]['ScanEachLayerParam']['FindSurface'])  # surface_judge
        out3[index_list3[0]].append(vvh_json[view]['RepeatTimes'])  # repeatTime
        out3[index_list3[1]].append(vvh_json[view]['DrivingTimeXYZ'][0])  # dirivingX
        out3[index_list3[2]].append(vvh_json[view]['DrivingTimeXYZ'][1])  # dirivingY
        out3[index_list3[3]].append(vvh_json[view]['DrivingTimeXYZ'][2])  # dirivingZ
        out3[index_list3[4]].append(vvh_json[view]['DrivingTimePiezo'])  # DrivingTimePiezo
        out3[index_list3[5]].append(vvh_json[view]['DampingTime'])  # DampingTime
        out3[index_list3[6]].append(vvh_json[view]['DrivingTimeAll'])  # DrivingTime
        out3[index_list3[7]].append(vvh_json[view]['ProcessTimeMain']['ElapsedTime'])  # 経過時間

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
            out1[index_list1[12]][L][id].append(int(not_txtdata[id][view].split(' ')[1]))   # not
            out1[index_list1[13]][L][id].append(float(not_txtdata[id][view].split(' ')[2])*1000)   # main_process
            out1[index_list1[14]][L][id].append(int(not_txtdata[id][view].split(' ')[3]))  # not_uncrust

    return out1, out2, out3


def check_flag(on: list, off: list):
    flags = {'ex': True, 'nog': True, 'nog0': True, 'nog15': True, 'toptobottom': True, 'not': True, 'not_un': True,
             'mainprocess': True, 'startpicnum': True, 'thickoflayer': True, 'base': True, 'freq': True, 'bright': True,
             'nog_all': True, 'text': True}
    if len(on) != 0 and len(off) != 0:
        sys.exit('hts2_plot.py: error: argument.\nCannot use "-on" and "-off" at the same time')
    elif len(on) != 0:
        # すべてFalseに
        for key in flags:
            flags[key] = False
        for content in on:
            flags[content] = True
    elif len(off) != 0:
        for content in off:
            flags[content] = False

    return flags


def text(array: np.ndarray, ax, color: str):
    for num_r, row in enumerate(array):
        for num_c, value in enumerate(array[num_r]):
            ax.text(num_c, num_r, '{:g}'.format(value), color=color, ha='center', va='center')


def textbox(ax, flat_list, ax_x_max, ax_y_max, under: int, over: int, *, factor: float = 0.9):
    entries = len(flat_list)
    mean = np.mean(flat_list)
    std_dev = np.std(flat_list)

    text = 'Entries: {:d}\nMean: {:4g}\nStd_dev: {:4g}\nUnderflow: {:d}\nOverflow: {:d}'.format(entries, mean, std_dev,
                                                                                                under, over)
    ax.text(ax_x_max * factor, ax_y_max * factor, text, bbox=(dict(boxstyle='square', fc='w')))


def append_area(input_data: list, scaned_area_view: int, sensor_pos_sorted: dict, step_x_num: int, step_y_num: int,
                mode: int):
    plot_array = [[], []]
    plot_array[0] = np.zeros((step_y_num * 9, step_x_num * 8))
    plot_array[1] = np.zeros((step_y_num * 9, step_x_num * 8))
    for i in range(scaned_area_view):
        # 1/3でY方向を3分割しているため何レーン目かを判断
        y_lane = math.floor(i / step_x_num) % 3
        for py in range(9):
            for px in range(8):
                pos = py * 8 + px
                id = sensor_pos_sorted[pos]['id']
                if id > 23:
                    continue
                if mode == 0:
                    tmp_l0 = input_data[0][id][i]
                    tmp_l1 = input_data[1][id][i]
                elif mode == 1:
                    tmp_l0 = input_data[0][i]
                    tmp_l1 = input_data[1][i]
                else:
                    sys.exit('mode error in \"append_area\"')
                # 全pcolermesh座標系におけるx,yの計算
                array_x_l0 = (i % step_x_num) * 8 + px  # xはviewのx座標とpxで計算
                array_x_l1 = (step_x_num - 1 - (i % step_x_num)) * 8 + px  # l1側はviewの順序を反転
                array_y = math.floor(
                    i / (step_x_num * 3)) * 9 + py + y_lane  # yはstep_x_numの三倍の商がフルセンサーのview_y + ３回のうち何回目か
                plot_array[0][array_y][array_x_l0] = tmp_l0
                plot_array[1][array_y][array_x_l1] = tmp_l1

    return plot_array


def append_sensor_array(average_data: list, sensor_pos_sorted: dict, *, mode: int = 0, z_max: list = None):
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
                    if mode == 1:
                        z[L][py][px] = average_data[L][id] / z_max[L]
                    else:
                        z[L][py][px] = average_data[L][id]

    return z


def meshplot_area(fig, pos: int, x: list, y: list, z: list, zmin: float, zmax: float, cmap, title: str, xlabel: str, ylabel: str, *, aspect_mode: bool = False):
    ax = fig.add_subplot(pos, title=title)
    z_ber = ax.pcolormesh(x, y, z, cmap=cmap, vmin=zmin, vmax=zmax)
    divider = make_axes_locatable(ax)  # axに紐付いたAxesDividerを取得
    cax = divider.append_axes("right", size="5%", pad=0.1)  # append_axesで新しいaxesを作成
    fig.colorbar(z_ber, orientation="vertical", cax=cax)
    if aspect_mode:
        ax.set_aspect('equal')
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)

    return ax


def meshplot_sensor(fig, pos: int, x: list, y: list, z: np.ndarray, zmin: float, zmax: float, cmap, title: str):
    ax = fig.add_subplot(pos, title=title)
    z_ber = ax.pcolormesh(x, y, z, cmap=cmap, vmin=zmin, vmax=zmax, edgecolors="black")
    text(z, ax, 'black')
    divider0 = make_axes_locatable(ax)  # axに紐付いたAxesDividerを取得
    cax0 = divider0.append_axes("right", size="5%", pad=0.1)  # append_axesで新しいaxesを作成
    fig.colorbar(z_ber, orientation="vertical", cax=cax0)

    return ax


def hist(fig, flat_data: list, pos: int, bins: int, zmin: float, zmax:float, title: str, color: str, *, xlabel: str = None, factor: float = 0.9):
    ax = fig.add_subplot(pos, title=title)
    hist_return = ax.hist(flat_data, histtype='step', bins=bins, range=(zmin, zmax), color='w', ec=color)
    under = np.count_nonzero(np.asarray(flat_data) < zmin)
    over = np.count_nonzero(np.asarray(flat_data) > zmax)
    if not xlabel == None:
        ax.set_xlabel(xlabel)
    textbox(ax, flat_data, zmax, max(hist_return[0]), under, over, factor=factor)

    return ax


def plot_area(input_data: list, zmin: float, zmax: float, step_x_num: int, step_y_num: int, title: str,
              sensor_pos_sorted: dict or list, out_file: str, startX: float, startY: float, mode: int, *, bins: int = 100):
    cmap = copy.copy(plt.get_cmap("jet"))
    cmap.set_under('w', 0.0001)  # 下限以下の色を設定

    if zmax - zmin < float(bins):
        bins = int(zmax - zmin)
    scaned_ara_view = step_x_num * step_y_num * 3  # step数から計算。1/3モードのため、view数は3倍

    plot_array = append_area(input_data, scaned_ara_view, sensor_pos_sorted, step_x_num, step_y_num, mode)

    x = np.arange(step_x_num * 8)
    x = x * step_x / 8 + startX
    y = np.arange(step_y_num * 9)
    y = y * step_y / 9 + startY
    x, y = np.meshgrid(x, y)

    fig = plt.figure(figsize=(11.69, 8.27), tight_layout=True)
    fig.suptitle(title, fontsize=20)
    ax1 = meshplot_area(fig, 221, x, y, plot_array[0], zmin, zmax, cmap, 'Layer0', 'X [mm]', 'Y [mm]',
                            aspect_mode=True)

    ax2 = meshplot_area(fig, 222, x, y, plot_array[1], zmin, zmax, cmap, 'Layer1', 'X [mm]', 'Y [mm]',
                            aspect_mode=True)

    flat_data_l0 = list(itertools.chain.from_iterable(plot_array[0]))
    ax3 = hist(fig, flat_data_l0, 223, bins, zmin, zmax, 'Layer0', 'r')

    flat_data_l1 = list(itertools.chain.from_iterable(plot_array[1]))
    ax4 = hist(fig, flat_data_l1, 224, bins, zmin, zmax, 'Layer1', 'b')

    plt.savefig(out_file, dpi=300)
    plt.clf()
    plt.close()
    print('{} written'.format(out_file))


def plot_base(input_data: list, zmin0: float, zmax0: float, zmin1: float, zmax1: float, basemin: float, basemax: float,
              step_x_num: int,
              step_y_num: int, title: str, sensor_pos_sorted: dict or list, out_file: str, *, bins: int = 100,
              basebins: int = 100):
    cmap = copy.copy(plt.get_cmap("jet"))
    cmap.set_under('w', 0.0001)  # 下限以下の色を設定

    scaned_ara_view = step_x_num * step_y_num * 3  # step数から計算。1/3モードのため、view数は3倍

    plot_array = append_area(input_data, scaned_ara_view, sensor_pos_sorted, step_x_num, step_y_num, 0)

    x = np.arange(step_x_num * 8)
    x = x * step_x / 8
    y = np.arange(step_y_num * 9)
    y = y * step_y / 9
    x, y = np.meshgrid(x, y)

    fig = plt.figure(figsize=(8.27 * 1.5, 11.69 * 1.5), tight_layout=True)
    fig.suptitle(title, fontsize=20)
    ax1 = meshplot_area(fig, 321, x, y, plot_array[0], zmin0, zmax0, cmap, 'Z of base surface Layer0', 'X [mm]',
                            'Y [mm]', aspect_mode=True)

    ax2 = meshplot_area(fig, 322, x, y, plot_array[1], zmin1, zmax1, cmap, 'Z of base surface Layer1', 'X [mm]',
                            'Y [mm]', aspect_mode=True)

    flat_data_l0 = list(itertools.chain.from_iterable(plot_array[0]))
    ax3 = hist(fig, flat_data_l0, 323, bins, zmin0, zmax0, 'Z of base surface Layer0', color='r', xlabel='Z0 [um]',
               factor=0.99)

    flat_data_l1 = list(itertools.chain.from_iterable(plot_array[1]))
    ax3 = hist(fig, flat_data_l1, 324, bins, zmin1, zmax1, 'Z of base surface Layer1', color='b', xlabel='Z1 [um]',
               factor=0.99)

    ax5 = meshplot_area(fig, 325, x, y, plot_array[1] - plot_array[0], basemin, basemax, cmap, 
                            'Thickness of Base (2D)', 'X [mm]', 'Y [mm]', aspect_mode=True)

    flat_data_base = list(itertools.chain.from_iterable(plot_array[1] - plot_array[0]))
    ax6 = hist(fig, flat_data_base, 326, basebins, basemin, basemax, 'Thickness of Base', 'r', xlabel='base [um]', 
               factor=0.95)

    plt.savefig(out_file, dpi=300)
    plt.clf()
    plt.close()
    print('{} written'.format(out_file))

    return flat_data_base


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

    z = append_sensor_array(average_data, sensor_pos_sorted)

    fig = plt.figure(figsize=(11.69, 8.27), tight_layout=True)
    fig.suptitle(title, fontsize=20)
    ax0 = meshplot_sensor(fig, 221, x, y, z[0], zmin, zmax, cmap, 'Layer0 array')

    ax1 = meshplot_sensor(fig, 222, x, y, z[1], zmin, zmax, cmap, 'Layer1 array')

    ax2 = fig.add_subplot(223, title='Layer0')
    x = np.arange(24)
    ax2.plot(x, average_data[0], marker='x', c='r')
    ax2.set_ylim(zmin, zmax)
    ax2.set_xticks(x)
    ax2.grid()

    ax3 = fig.add_subplot(224, title='Layer1')
    x = np.arange(24)
    ax3.plot(x, average_data[1], marker='x', c='b')
    ax3.set_ylim(zmin, zmax)
    ax3.set_xticks(x)
    ax3.grid()

    plt.savefig(out_file, dpi=300)
    plt.clf()
    plt.close()
    print('{} written'.format(out_file))


def plot_sensor_not(input_data: list, title: str,
                    sensor_pos_sorted: dict or list, out_file: str, *, relative_min: float = 0.8,
                    absolute_max: float = 30000):
    average_data = [[], []]
    for i in range(len(input_data[0])):
        for L in range(2):
            average_data[L].append(np.average(input_data[L][i]))

    cmap = copy.copy(plt.get_cmap("copper"))
    cmap.set_under('w', 0.0001)  # 下限以下の色を設定
    x = np.arange(8)
    y = np.arange(9)
    x, y = np.meshgrid(x, y)
    not_max = [max(average_data[0]), max(average_data[1])]

    z = append_sensor_array(average_data, sensor_pos_sorted, mode=1, z_max=not_max)

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
    ax3 = meshplot_sensor(fig, 323, x, y, z[0], relative_min, 1, cmap, 'Layer0  (relative, sensor array)')

    ax4 = meshplot_sensor(fig, 324, x, y, z[1], relative_min, 1, cmap, 'Layer1  (relative, sensor array)')

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
    plt.clf()
    plt.close()
    print('{} written'.format(out_file))


def plot_nogall(input_nogdata: list, imager_id: int, plot_ymax: float, nog_thr_list: list, out_path: str, *,
                alpha: float = 0.15):
    title = 'All nog Plot Imager = {}'.format(imager_id)
    color = ['r', 'b']
    cmap = plt.get_cmap('rainbow')
    fig = plt.figure(tight_layout=True)
    fig.suptitle(title, fontsize=20)
    pos = 121
    for layer in range(len(nog_thr_list)):
        ax = fig.add_subplot(pos)
        for i in range(len(input_nogdata[layer][imager_id])):
            ax.plot(input_nogdata[layer][imager_id][i], marker='x', ms=0.5, lw=0.5,
                    color=cmap(i / len(input_nogdata[layer][imager_id])),
                    markerfacecolor=cmap(i / len(input_nogdata[layer][imager_id])), alpha=alpha)
        Npic_Snap = len(input_nogdata[layer][imager_id][0])
        ax.set_xlabel('picture number \n ←lens         stage→')
        ax.set_ylabel('Number of grains')
        ax.set_xlim(0, Npic_Snap - 1)  # x軸の範囲
        ax.set_ylim(0, plot_ymax)
        ax.set_title('Number of Grain Layer = {}'.format(layer))
        for j in range(len(nog_thr_list[layer])):
            ax.axhline(y=nog_thr_list[layer][j], color=color[j])
        pos += 1

    out_file = os.path.join(out_path, 'all_nog_plot_{}.png'.format(imager_id))
    plt.savefig(out_file, dpi=300)
    print('{} written'.format(out_file))


def plot_elaspedtime(input_data: list, out_path: str):
    plt.plot(input_data, marker=None)
    plt.xlabel('Number of views')
    plt.ylabel('ElaspedTime [s]')
    plt.grid()

    out_file = os.path.join(out_path, 'ElaspedTime.png')
    plt.savefig(out_file, dpi=300)
    print('{} written'.format(out_file))


def calc_df(input_df: dict):
    out = pd.DataFrame(input_df)
    view_time = []
    Hz_list = []
    for i in range(len(out)):
        if i == len(out) - 1:
            view_time.append(None)
            Hz_list.append(None)
            continue
        dff_time = out['ElapsedTime'][i + 1] - out['ElapsedTime'][i]
        view_time.append(dff_time)
        Hz = 1 / dff_time
        Hz_list.append(Hz)
    out['view_time'] = view_time
    out['Hz'] = Hz_list

    return out


def plot_frequency(input_df: pd.DataFrame, out_path: str, *, plotmin: float = 0, plotmax: float = 6):
    fig = plt.figure(figsize=(8.27, 11.69), tight_layout=True)
    fig.suptitle('Frequency (RepeatTime = 0)')
    ax1 = fig.add_subplot(211)
    ax1.plot(input_df.query('repeatTime == 0')['Hz'], 'x', ms=0.7)
    ax1.set_xlabel('Number of view')
    ax1.set_ylabel('Frequency [Hz]')
    ax1.set_ylim(plotmin, plotmax)
    ax1.grid()

    ax2 = fig.add_subplot(212)
    ax2.hist(input_df.query('repeatTime == 0')['Hz'], bins=100, range=(plotmin, plotmax), histtype='stepfilled',
             facecolor='yellow',
             linewidth=1, edgecolor='black')
    ax2.set_xlabel('Frequency [Hz]')
    ax2.grid()

    plt.savefig(os.path.join(out_path, 'Frequency.png'), dpi=300)
    plt.clf()
    plt.close()
    print('{} written'.format(os.path.join(out_path, 'Frequency.png')))


def plot_TargetBright(evmg_json: dict, sensor_pos_sorted: dict or list, out_path: str):
    brightlist = []
    for i in range(len(evmg_json['ImagerControllerParamList'])):
        brightlist.append(evmg_json['ImagerControllerParamList'][i]['TargetBrightness'])

    cmap = copy.copy(plt.get_cmap("jet"))
    cmap.set_under('w', 1)  # 下限以下の色を設定
    x = np.arange(8)
    y = np.arange(9)
    x, y = np.meshgrid(x, y)
    z = np.zeros((9, 8))
    for py in range(9):
        for px in range(8):
            id = sensor_pos_sorted[py * 8 + px]['id']
            if id > 23:
                z[py][px] = 0
            else:
                z[py][px] = brightlist[id]

    fig = plt.figure()
    ax0 = plt.subplot(title='Target brightness')
    z_ber0 = ax0.pcolormesh(x, y, z, cmap=cmap, vmax=256, vmin=200, edgecolors="black")
    text(z, ax0, 'black')
    divider0 = make_axes_locatable(ax0)  # axに紐付いたAxesDividerを取得
    cax0 = divider0.append_axes("right", size="5%", pad=0.1)  # append_axesで新しいaxesを作成
    pp0 = fig.colorbar(z_ber0, orientation="vertical", cax=cax0)

    outfile = os.path.join(out_path, 'TargetBrightness.png')
    plt.savefig(outfile, dpi=300)
    print('{} written'.format(outfile))


def text_dump(data1: dict, data2: dict, out_path: str):
    outfile = os.path.join(out_path, 'summary.txt')
    with open(outfile, 'w') as f:
        for i in range(2):
            print('Layer {}'.format(i), file=f)
            print('{:33}:  {:g}'.format('Ave. Exposure Count', np.mean(data1['excount'][i])), file=f)
            print('{:33}:  {:g}'.format('Ave. Number of Grains', np.mean(data1['nog_over_thr'][i])), file=f)
            print('{:33}:  {:g}'.format('Ave. Number of Tracks', np.mean(data1['not'][i])), file=f)
            print('{:33}:  {:g}'.format('Ave. Thick Of Layer', np.mean(data2['ThickOfLayer'][i])), file=f)
            print('{:33}:  {:d} / {:d}'
                  .format('Number of false of surface judge',
                          np.count_nonzero(data2['surf_judge'][i] == False), len(data2['surf_judge'][i])), file=f)
            flat_top2bottom = np.asarray(list(itertools.chain.from_iterable(data1['top2bottom'][i])))
            print('{:33}:  {:d} / {:d}'.format('Number of thin (bottom-top<16)', np.count_nonzero(flat_top2bottom < 16),
                                                                       len(data1['top2bottom'][i]) *
                                                                       len(data1['top2bottom'][i][0])), file=f)
            print('', file=f)

        base_thickness = np.asarray(data1['fine_z'][1]) - np.asarray(data1['fine_z'][0])
        print('{:33}:  {:g}'.format('Ave. Thickness of base', np.mean(base_thickness)), file=f)
