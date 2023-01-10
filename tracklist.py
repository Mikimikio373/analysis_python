import pandas as pn
from matplotlib import pyplot as plt

csvpath = 'Y:\\Mikio\\mine\\powerpoint\\F2F\\20230106\\data\\tracklist.csv'
track_pn = pn.read_csv(csvpath)
dx = []
dy = []
dax = []
day = []

for i in range(0, len(track_pn)):
    for j in range(i, len(track_pn)):
        if track_pn["id00"][i] == track_pn["id10"][i]:
            dx.append(track_pn["x0"][i] - track_pn["x1"][i])
            dy.append(track_pn["y0"][i] - track_pn["y1"][i])
            dax.append(track_pn["ax0"][i] - track_pn["ax1"][i])
            day.append(track_pn["ay0"][i] - track_pn["ay1"][i])

print(dx)
print(dy)
print(len(dx), len(dy))
plt.hist2d(dx, dy, bins=100)
plt.show()