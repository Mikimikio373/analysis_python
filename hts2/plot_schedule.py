import numpy as np
import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd

date_list = []
scan_num_list = []
scan_num = 0
start_day = datetime.datetime.strptime("2023-11-6", '%Y-%m-%d')
date = start_day
endtime1 = datetime.datetime.strptime('2023-12-27', '%Y-%m-%d')
while date < endtime1:
    scan_num += 20.0 / 7
    scan_num_list.append(scan_num)
    date_list.append(date)
    date += datetime.timedelta(days=1)

endtime2 = datetime.datetime.strptime('2024-1-6', '%Y-%m-%d')
while date < endtime2:
    scan_num += 0
    scan_num_list.append(scan_num)
    date_list.append(date)
    date += datetime.timedelta(days=1)

endtime3 = datetime.datetime.strptime('2024-2-1', '%Y-%m-%d')
while date < endtime3:
    scan_num += 45 / 7
    scan_num_list.append(scan_num)
    date_list.append(date)
    date += datetime.timedelta(days=1)

while scan_num <= 1800:
    scan_num += 90 / 7
    # if scan_num > 1800:
    #     break
    scan_num_list.append(scan_num)
    date_list.append(date)
    date += datetime.timedelta(days=1)

print(max(scan_num_list))
height, x, ret = plt.hist(date_list, bins=len(date_list))
plt.clf()
fig = plt.figure(tight_layout=True)
ax = fig.add_subplot(111)
ax.hist(x[:-1], bins=x, weights=scan_num_list, edgecolor='g', hatch='\\\\', histtype='step')
ax.xaxis.set_major_locator(mdates.MonthLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y/%m/%d'))
ax.set_ylim(0, 1800)
ax.set_ylabel('合計読み取り枚数', fontname="MS Gothic", fontsize=12)
labels_x = ax.get_xticklabels()
labels_y = ax.get_yticklabels()
plt.setp(labels_x, rotation=45, fontsize=12)
plt.setp(labels_y, fontsize=12)
plt.savefig('B:/data/powerpoint/HTS2_data/4master_theisis/scan_schedule/pred.png', dpi=300)
# plt.show()


df = pd.read_csv('B:/data/powerpoint/HTS2_data/4master_theisis/scan_schedule/scan_prog_20240118.csv', header=None)

date_list1 = pd.to_datetime(df[0].values)
scan_num_list1 = df[1].values
scan_num = scan_num_list1[-1]
date = date_list1[-1]
scan_num_list2 = []
date_list2 = []
endtime1 = datetime.datetime.strptime('2024-1-31', '%Y-%m-%d')
while date < endtime1:
    scan_num += 45.0 / 7
    scan_num_list2.append(scan_num)
    date_list2.append(date)
    date += datetime.timedelta(days=1)
while scan_num <= 1800:
    scan_num += 90 / 7
    # if scan_num > 1800:
    #     break
    scan_num_list2.append(scan_num)
    date_list2.append(date)
    date += datetime.timedelta(days=1)

print(max(scan_num_list2))


height1, x1, ret1 = plt.hist(date_list1, bins=len(date_list1))
height2, x2, ret2 = plt.hist(date_list2, bins=len(date_list2))
plt.clf()
fig = plt.figure(tight_layout=True)
ax = fig.add_subplot(111)
ax.hist(x1[:-1], bins=x1, weights=scan_num_list1, edgecolor='b', hatch='\\\\', histtype='step')
ax.hist(x2[:-1], bins=x2, weights=scan_num_list2, edgecolor='r', hatch='\\\\', histtype='step')
ax.xaxis.set_major_locator(mdates.MonthLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y/%m/%d'))
ax.set_ylim(0, 1800)
ax.set_ylabel('合計読み取り枚数', fontname="MS Gothic", fontsize=12)
labels_x = ax.get_xticklabels()
labels_y = ax.get_yticklabels()
plt.setp(labels_x, rotation=45, fontsize=12)
plt.setp(labels_y, fontsize=12)
plt.savefig('B:/data/powerpoint/HTS2_data/4master_theisis/scan_schedule/result.png', dpi=300)
# plt.show()