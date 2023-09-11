import pandas as pd
from matplotlib import pyplot as plt
import os
import matplotlib.cm as cm

basepath = 'Q:/minami/20230911_nog_NRKR_tilt'
csv_path = os.path.join(basepath, 'xyz_fit.csv')
surf_fit = os.path.join(basepath, 'fit_surf.csv')

xyz_df = pd.read_csv(csv_path)
plt.scatter(xyz_df['x'], xyz_df['y'], c=xyz_df['z'])
plt.colorbar()
plt.savefig(os.path.join(basepath, '2d_z.png'), dpi=300)
plt.clf()

fit_df = pd.read_csv(surf_fit)
a0 = fit_df['a'][0]
b0 = fit_df['b'][0]
c0 = fit_df['c'][0]
a1 = fit_df['a'][1]
b1 = fit_df['b'][1]
c1 = fit_df['c'][1]
z_fix = []
for i in range(len(xyz_df['z'])):
    if xyz_df['flag'][i] == 0:
        fit_z = a0 * xyz_df['x'][i] + b0 * xyz_df['y'][i] + c0
    else:
        fit_z = a1 * xyz_df['x'][i] + b1 * xyz_df['y'][i] + c1
    tmp = xyz_df['z'][i] - fit_z
    z_fix.append(tmp)

plt.scatter(xyz_df['x'], xyz_df['y'], c=z_fix)
plt.colorbar()
plt.savefig(os.path.join(basepath, '2d_z_fix.png'), dpi=300)
plt.clf()
