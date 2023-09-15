import pandas as pd
import numpy as np

path = 'Q:/minami/20230914_Ali2/calc_ali/all_stage_list.csv'
out_path = 'Q:/minami/20230914_Ali2/calc_ali/0-3_all_list_fix.csv'

ref_pd = pd.read_csv(path)

fix_dx = -0.00054026
fix_dy = 0.000146075

pd_dx = np.asarray(ref_pd['X']).astype(np.float64)
pd_dy = np.asarray(ref_pd['Y']).astype(np.float64)
pd_flag = np.asarray(ref_pd['flag']).astype(np.int8)
pd_dx += fix_dx
pd_dy += fix_dy

out_pd = pd.DataFrame()
out_pd['X'] = pd_dx
out_pd['Y'] = pd_dy
out_pd['flag'] = pd_flag
out_pd.to_csv(out_path, index=False)
