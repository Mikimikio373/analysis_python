import json
import os
import sys
import math

import pandas as pd
import matplotlib.pyplot as plt


def erace_errdata(df: pd.DataFrame, *, sigma_min: float = 0.11, sigma_max: float = 0.25, height_cut: float = 1000):
    drop_index = []
    for i in range(len(df)):
        if df['sigma_dpx'][i] < sigma_min or df['sigma_dpx'][i] > sigma_max:
            drop_index.append(i)
        if df['sigma_dpy'][i] < sigma_min or df['sigma_dpy'][i] > sigma_max:
            drop_index.append(i)
        if df['height_dpx'][i] > height_cut:
            drop_index.append(i)
        if df['height_dpy'][i] > height_cut:
            drop_index.append(i)
    drop_index = list(set(drop_index))
    output = df.drop(df.index[drop_index])
    output = output.reset_index(drop=True)
    return output


def calc_fiterr(df: pd.DataFrame):
    dpxerr_list = []
    dpyerr_list = []
    for i in range(len(df)):
        dpxerr_list.append(df['sigma_dpx'][i] / math.sqrt(df['entries'][i]))
        dpyerr_list.append(df['sigma_dpy'][i] / math.sqrt(df['entries'][i]))

    df['dpx_err'] = dpxerr_list
    df['dpy_err'] = dpyerr_list
    return df

def edit_fitdata(csvpath: str ,vvh_path: str , origin_view: int = 0, xline_num: int = 100):

    # データの読み取り
    if not os.path.exists(csvpath):
        sys.exit('there is no file: {}'.format(csvpath))
    df = pd.read_csv(csvpath)
    df_cut = erace_errdata(df)  # fit時に失敗している個所の削除
    df_cut = calc_fiterr(df_cut)    # sigmaとentriesから誤差の計算

    if not os.path.exists(vvh_path):
        sys.exit('there si no file: {}'.format(vvh_path))
    with open(vvh_path, 'rb') as f:
        vvh = json.load(f)

    origin_sx = vvh[origin_view]['Positions0']['X']
    origin_sy = vvh[origin_view]['Positions0']['Y']

    dsx_list = []
    dsy_list = []
    for i in range(len(df_cut)):
        view = int(df_cut['vy'][i] * xline_num + df_cut['vx'][i])
        sx = vvh[view]['Positions0']['X']
        sy = vvh[view]['Positions0']['Y']
        dsx_list.append(sx - origin_sx)
        dsy_list.append(sy - origin_sy)

    df_cut['dsx'] = dsx_list
    df_cut['dsy'] = dsy_list
    #後でヒストグラムのプロットを作る

    out_csv = os.path.join(os.path.split(csvpath)[0], 'edit_fit_data.csv')
    df_cut.to_csv(out_csv, index=False)


# edit_fitdata()
