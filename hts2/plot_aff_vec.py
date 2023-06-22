import numpy as np
import pandas as pn
import matplotlib.pyplot as plt

csv_path = 'R:/minami/20230531_aff/Module1/sensor-7/GrainMatching_loop/fitdata_edit.csv'
affdata_path = 'R:/minami/20230531_aff/Module1/sensor-7/aff_data.csv'

fit_df = pn.read_csv(csv_path)
fit_df = fit_df.drop(columns=fit_df.columns[0])
print(fit_df)

aff_df = pn.read_csv(affdata_path)
print(aff_df)

pred_sx_all = []
pred_sy_all = []
esx_list = []
esy_list = []

for i in range(len(fit_df)):
    pred_sx = aff_df['a'][0] * fit_df['meanX'][i] + aff_df['b'][0] * fit_df['meanY'][i]
    pred_sy = aff_df['c'][0] * fit_df['meanX'][i] + aff_df['d'][0] * fit_df['meanY'][i]
    esx = fit_df['dsx'][i] - pred_sx
    esy = fit_df['dsy'][i] - pred_sy

    pred_sx_all.append(pred_sx)
    pred_sy_all.append(pred_sy)
    esx_list.append(esx)
    esy_list.append(esy)

plt.quiver(fit_df['meanX'], fit_df['meanY'], esx_list, esy_list, color='red', angles='xy', scale_units='xy')
plt.show()

fit_df['pred_sx'] = pred_sx_all
fit_df['pred_sy'] = pred_sy_all
fit_df['esx'] = esx_list
fit_df['esy'] = esy_list
out_csv = 'R:/minami/20230531_aff/Module1/sensor-7/fitdata_err.csv'
fit_df.to_csv(out_csv, index=False)

# aff = [[aff_df['a'][0], aff_df['b'][0]], [aff_df['c'][0], aff_df['d'][0]]]
# aff_inv = np.linalg.inv(aff)
#
# pred_px_all = []
# pred_py_all = []
# epx_list = []
# epy_list = []
#
# for i in range(len(fit_df)):
#     pred_px = aff_inv[0][0] * fit_df['dsx'][i] + aff[0][1] * fit_df['dsy'][i]
#     pred_py = aff_inv[1][0] * fit_df['dsx'][i] + aff[1][1] * fit_df['dsy'][i]
#     epx = fit_df['meanX'][i] - pred_px
#     epy = fit_df['meanY'][i] - pred_py
#
#     pred_px_all.append(pred_px)
#     pred_py_all.append(pred_py)
#     epx_list.append(epx)
#     epy_list.append(epy)
#
# plt.quiver(fit_df['dsx'], fit_df['dsy'], epx_list, epy_list, color='red', angles='xy', scale_units='xy', scale=50000)
# plt.show()