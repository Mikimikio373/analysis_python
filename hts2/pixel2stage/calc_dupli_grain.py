import pandas as pd

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

count = 0
for i in range(len(df1)):
    for j in range(len(df2)):
        if abs(df1['X'][i] - df2['X'][j]) < 0.00063 and abs(df1['Y'][i] - df2['Y'][j]) < 0.00063:
            count += 1
            break

print(len(df1))
print(len(df2))
print(count)