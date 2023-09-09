import pandas as pd

path1 = 'R:/minami/20230531_aff/Module1/sensor-7/pixel2stage/0-0_stage.csv'
path2 = 'R:/minami/20230531_aff/Module1/sensor-7/pixel2stage/40-0_stage.csv'

df1 = pd.read_csv(path1)
df2 = pd.read_csv(path2)

dx_list = []
dy_list = []

for i in range(len(df1)):
    for j in range(len(df2)):
        dx = df2['X'][j] - df1['X'][i]
        dy = df2['Y'][j] - df1['Y'][i]
        dx_list.append(dx)
        dy_list.append(dy)
    print('i: {}/{} ended'.format(i, len(df1)))

out_df = pd.DataFrame()
out_df['dx'] = dx_list
out_df['dy'] = dy_list
out_df.to_csv('R:/minami/20230531_aff/Module1/sensor-7/pixel2stage/0-0vs40-0_stage.csv', index=False)