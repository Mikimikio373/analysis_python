import pandas as pd
from matplotlib import pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

pdf = PdfPages('R:/minami/20230531_aff/Module1/sensor-7/pixel2stage/testplot_0-0_10.pdf')

path1 = 'R:/minami/20230531_aff/Module1/sensor-7/pixel2stage/0-0_stage.csv'
path2 = 'R:/minami/20230531_aff/Module1/sensor-7/pixel2stage/0-0_1_stage.csv'
path3 = 'R:/minami/20230531_aff/Module1/sensor-7/pixel2stage/0-0_2_stage.csv'
path4 = 'R:/minami/20230531_aff/Module1/sensor-7/pixel2stage/0-0_3_stage.csv'
path5 = 'R:/minami/20230531_aff/Module1/sensor-7/pixel2stage/0-0_4_stage.csv'
path6 = 'R:/minami/20230531_aff/Module1/sensor-7/pixel2stage/0-0_5_stage.csv'
path7 = 'R:/minami/20230531_aff/Module1/sensor-7/pixel2stage/0-0_6_stage.csv'
path8 = 'R:/minami/20230531_aff/Module1/sensor-7/pixel2stage/0-0_7_stage.csv'
path9 = 'R:/minami/20230531_aff/Module1/sensor-7/pixel2stage/0-0_8_stage.csv'
path10 = 'R:/minami/20230531_aff/Module1/sensor-7/pixel2stage/0-0_9_stage.csv'

df1 = pd.read_csv(path1)
df2 = pd.read_csv(path2)
df3 = pd.read_csv(path3)
df4 = pd.read_csv(path4)
df5 = pd.read_csv(path5)
df6 = pd.read_csv(path6)
df7 = pd.read_csv(path7)
df8 = pd.read_csv(path8)
df9 = pd.read_csv(path9)
df10 = pd.read_csv(path10)

fig = plt.figure()
ax = fig.add_subplot(111, title='hit pixel map', xlabel='stage x [mm]', ylabel='stage y [mm]')
# ax.scatter(df1['X'], df1["Y"], marker='o', s=2, c='r', alpha=0.5, label='(0, 0)')
# ax.scatter(df2['X'], df2['Y'], marker='o', s=2, c='b', alpha=0.5, label='(1 mm, 0)')

ax.scatter(df1['X'], df1["Y"], marker='o', s=2, alpha=0.5, label='1')
ax.legend(fontsize="xx-small", loc='upper left', bbox_to_anchor=(1, 1))
pdf.savefig()
ax.scatter(df2['X'], df2["Y"], marker='o', s=2, alpha=0.5, label='2')
ax.legend(fontsize="xx-small", loc='upper left', bbox_to_anchor=(1, 1))
pdf.savefig()
ax.scatter(df3['X'], df3["Y"], marker='o', s=2, alpha=0.5, label='3')
ax.legend(fontsize="xx-small", loc='upper left', bbox_to_anchor=(1, 1))
pdf.savefig()
ax.scatter(df4['X'], df4["Y"], marker='o', s=2, alpha=0.5, label='4')
ax.legend(fontsize="xx-small", loc='upper left', bbox_to_anchor=(1, 1))
pdf.savefig()
ax.scatter(df5['X'], df5["Y"], marker='o', s=2, alpha=0.5, label='5')
ax.legend(fontsize="xx-small", loc='upper left', bbox_to_anchor=(1, 1))
pdf.savefig()
ax.scatter(df6['X'], df6["Y"], marker='o', s=2, alpha=0.5, label='6')
ax.legend(fontsize="xx-small", loc='upper left', bbox_to_anchor=(1, 1))
pdf.savefig()
ax.scatter(df7['X'], df7["Y"], marker='o', s=2, alpha=0.5, label='7')
ax.legend(fontsize="xx-small", loc='upper left', bbox_to_anchor=(1, 1))
pdf.savefig()
ax.scatter(df8['X'], df8["Y"], marker='o', s=2, alpha=0.5, label='8')
ax.legend(fontsize="xx-small", loc='upper left', bbox_to_anchor=(1, 1))
pdf.savefig()
ax.scatter(df9['X'], df9["Y"], marker='o', s=2, alpha=0.5, label='9')
ax.legend(fontsize="xx-small", loc='upper left', bbox_to_anchor=(1, 1))
pdf.savefig()
ax.scatter(df10['X'], df10["Y"], marker='o', s=2, alpha=0.5, label='10')
ax.legend(fontsize="xx-small", loc='upper left', bbox_to_anchor=(1, 1))
pdf.savefig()
pdf.close()

# plt.show()
# plt.savefig('R:/minami/20230531_aff/Module1/sensor-7/pixel2stage/testplot_0-0_10.pdf')