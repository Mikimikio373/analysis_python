import pandas as pd
import matplotlib.pyplot as plt

hts_path = 'B:/data/powerpoint/ICMaSS/data/accdata_RL_hts.csv'
hts2_path = 'B:/data/powerpoint/ICMaSS/data/accdata_RL_hts2.csv'

hts = pd.read_csv(hts_path, header=None)
hts2 = pd.read_csv(hts2_path, header=None)

fig, ax = plt.subplots(tight_layout=True)
plt.plot(hts[0], hts[2], 'o', ms=8, mew=1.5, mfc='None', label='HTS-lateral')
plt.plot(hts[0], hts[1], 's', ms=8, mew=1.5, mfc='None', label='HTS-radial')
plt.plot(hts2[0], hts2[2], '^', ms=8, mew=1.5, mfc='None', label='HTS2-lateral')
plt.plot(hts2[0], hts2[1], 'v', ms=8, mew=1.5, mfc='None', label='HTS2-radial')
plt.xlabel('angle (tanΘ)', fontsize=18)
plt.ylabel('δ(dtanΘ)', fontsize=18)
plt.legend(fontsize=18)
plt.setp(ax.get_xticklabels(), fontsize=15)
plt.setp(ax.get_yticklabels(), fontsize=15)
plt.grid()
# plt.show()
plt.savefig('B:/data/powerpoint/ICMaSS/data/plot_RL.png', dpi=300)

