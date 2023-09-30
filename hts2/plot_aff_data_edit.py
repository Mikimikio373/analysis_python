import matplotlib.pyplot as plt
import pandas as pd

csv_path = 'Q:/minami/20230912_aff/Module0/sensor-3/fitdata_edit.csv'
df = pd.read_csv(csv_path)
print(df)

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(df['meanX'], df['meanY'], df['dsx'], marker='o', c='r', alpha=1)
# ax.set_xlabel('pixel X [pixel]')
# ax.set_ylabel('pixel Y [pixel]')
# ax.set_zlabel('stage X [mm]')
plt.show()
