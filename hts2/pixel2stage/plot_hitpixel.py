import pandas as pd
from matplotlib import pyplot as plt


path1 = 'R:/minami/20230531_aff/Module1/sensor-7/pixel2stage/test0-0_stage.csv'
path2 = 'R:/minami/20230531_aff/Module1/sensor-7/pixel2stage/test40-0_stage.csv'

df1 = pd.read_csv(path1)
df2 = pd.read_csv(path2)

fig = plt.figure()
ax = fig.add_subplot(111, title='hit pixel map', xlabel='stage x [mm]', ylabel='stage y [mm]')
ax.scatter(df1['X'], df1["Y"], marker='o', s=2, c='r', alpha=0.3, label='(0, 0)')
ax.scatter(df2['X'], df2['Y'], marker='o', s=2, c='b', alpha=0.3, label='(1 mm, 0)')
ax.legend()
# plt.show()
plt.savefig('R:/minami/20230531_aff/Module1/sensor-7/pixel2stage/testplot.pdf')