import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

csv_path1 = 'Q:/minami/20220429_suganami/006/IMAGE00_AREA-1/png_thr_dilate/png_thr10_9/area_list_l0.csv'
csv_path2 = 'R:/usuda/GRAINE2023_u4/PL088_0904gap4/IMAGE00_AREA-1/png_thr_dilate/png_thr10_9/area_list_l0.csv'
csv_path3 = 'R:/usuda/GRAINE2023_u4/PL088_0904gap4/IMAGE00_AREA-1/png_thr_dilate/png_thr_cubic10_9_zfilt-0.15/area_list_l0.csv'

# csv_path1 = 'Q:/minami/20220429_suganami/006/IMAGE00_AREA-1/png_thr_nolilate/png_thr10_9/area_list_l0.csv'
# csv_path2 = 'R:/usuda/GRAINE2023_u4/PL088_0904gap4/IMAGE00_AREA-1/png_thr_nogdilate/png_thr10_9/area_list_l0.csv'
# csv_path3 = 'R:/usuda/GRAINE2023_u4/PL088_0904gap4/IMAGE00_AREA-1/png_thr_nogdilate/png_thr_cubic10_9_zfilt-0.15/area_list_l0.csv'

df1 = pd.read_csv(csv_path1)
views1 = 18 * 37
size1 = len(df1)
df2 = pd.read_csv(csv_path2)
views2 = 27 * 55
size2 = len(df2)
df3 = pd.read_csv(csv_path3)
views3 = 27 * 55
size3 = len(df3)


scale = float(size1/size2)


x_width = 100
# plt.hist(df1['L0'], bins=x_width, range=(0.5, x_width+0.5), log=True, color='b', label='NRKR', alpha=0.3, weights=np.ones_like(df1['L0'])/views1)
plt.hist(df2['L0'], bins=x_width, range=(0.5, x_width+0.5), log=True, color='r', label='GRAINE2023', alpha=0.3, weights=np.ones_like(df2['L0'])/views2)
plt.hist(df3['L0'], bins=x_width, range=(0.5, x_width+0.5), log=True, color='y', label='GRAINE2023_cubic', alpha=0.3, weights=np.ones_like(df3['L0'])/views2)
plt.title('Frequency of object size / 1 view', fontsize=20)
plt.xlabel('Area of objects [pixel]', fontsize=14)
plt.ylabel('Entries', fontsize=14)
plt.tick_params(labelsize=14)
plt.legend(fontsize=14)
plt.ylim(0.5, 10000)
# plt.show()
# plt.savefig('B:/data/powerpoint/HTS2_meeting/20231204/fig/objnum_dilate.png', dpi=300)
plt.savefig('B:/data/powerpoint/HTS2_meeting/20231204/fig/objnum_dilate_graine.png', dpi=300)
# plt.savefig('B:/data/powerpoint/HTS2_meeting/20231204/fig/objnum_nondilate.png', dpi=300)
# plt.savefig('B:/data/powerpoint/HTS2_meeting/20231204/fig/objnum_nondilate_graine.png', dpi=300)
