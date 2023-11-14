import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

import check_stage_module as mylib

# path1 = 'P:/usuda/u19-003-a1/ali.json'
# mylib.plot_xydivide(path1, 'B:/data/powerpoint/HTS2_meeting/20231115/fig/ali_u19-003-a1_xydivide.pdf')

path1 = 'P:/usuda/u19-003-a1/ali.json'
path2 = 'P:/usuda/u19-003-a2/ali.json'
# path1 = 'A:/Test/check_stage/20231108_small_acrylic/ali.json'
# path2 = 'A:/Test/check_stage/20231111_graine_acrylic/ali.json'

shift_data1, int_df1, stage1 = mylib.read_ali_stage(path1)
shift_data2, int_df2, stage2 = mylib.read_ali_stage(path2)
# print(shift_data1[0][shift_data1[0]['V'] > 0.005])

pdf = PdfPages('B:/data/powerpoint/HTS2_meeting/20231115/fig/u19-003-a1-2.pdf')

# print(len(shift_data1[layer]), len(shift_data2[layer]))
for layer, flag, title in zip([0, 1], [1, 2], ['X overlap', 'Y overlap']):
    marge = pd.merge(shift_data1[layer], shift_data2[layer], how="inner", on=["X", "Y"])

    X = marge.query('flag_x == {}'.format(flag))['X']
    Y = marge.query('flag_x == {}'.format(flag))['Y']
    U = marge.query('flag_x == {}'.format(flag))['U_x'] - marge.query('flag_x == {}'.format(flag))['U_y']
    V = marge.query('flag_x == {}'.format(flag))['V_x'] - marge.query('flag_x == {}'.format(flag))['V_y']
    stage_x = sorted(list(set(stage1[layer]["stage_x"])))
    stage_y = sorted(list(set(stage1[layer]["stage_y"])))

    fig = plt.figure()
    ax = fig.add_subplot(111)

    mylib.plot_stage_shift_vec(ax, pdf, X, Y, U, V, stage_x, stage_y, 'layer = {} ({})'.format(layer, title))
    mylib.plot_stage_shift_scatter(fig, pdf, X, Y, U, V, 'layer = {} ({})'.format(layer, title))
    plt.clf()
pdf.close()
