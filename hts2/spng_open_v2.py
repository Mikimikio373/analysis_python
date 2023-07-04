import cv2
import numpy as np
import json
import sys
import os
import yaml

# basepath = 'R:\\minami\\20230603_ali-z\\Module0\\sensor-6'
if len(sys.argv) != 2:
    exit('command line error. please \"basepath\"')

basepath = sys.argv[1]
image = 'IMAGE00_AREA-1'
areapath = os.path.join(basepath, image)
os.chdir(basepath)
current_dir = os.getcwd()
print('now dir: ', current_dir)
yaml_path = 'AreaScan4Param.yml'
with open(yaml_path, 'rb') as yml:
    param = yaml.safe_load(yml)
folder = 'png'
working_direc = 'IMAGE00_AREA-1'
os.chdir(working_direc)
path = os.getcwd()
print('path changed.')
print('currend path = ', path)

if os.path.exists(folder):
    print("This folder already exists. Can I overwrite it? Press \'y\' as Yes or \'n\' as No")
    answer = input()
    if answer == "y":
        os.makedirs(folder, exist_ok=True)
    else:
        print("this program ended")
        sys.exit()

else:
    os.makedirs(folder)

x_size = param['Area'][0]['NViewX']  # x方向の大きさ
y_size = param["Area"][0]["NViewY"]  # y方向の大きさ
layer = param["Area"][0]["NLayer"]
npicture = param["NPictures"]
plate_sum = layer * x_size * y_size

n = 0
while n < plate_sum:
    for y in range(0, y_size):
        for top_down in range(0, layer):
            for x in range(0, x_size):
                json_open = open('V{0:08d}_L{3:d}_VX{1:04d}_VY{2:04d}_0_{4:03d}.json'.format(n, x, y, top_down, npicture), 'r')
                f = open("V{0:08d}_L{3:d}_VX{1:04d}_VY{2:04d}_0_{4:03d}.spng".format(n, x, y, top_down, npicture), "rb")
                json_load = json.load(json_open)
                n += 1

                folder2 = 'L{0}_VX{1:04}_VY{2:04}'.format(top_down, x, y)
                os.makedirs(os.path.join(folder, folder2), exist_ok=True)

                for i in range(0, len(json_load['Images'])):
                    filename = json_load['Images'][i]['Path']
                    filename_split = filename.split('&')
                    filesize = int(filename_split[-1])
                    data = np.fromfile(f, np.uint8, filesize, "", 8)
                    dst = cv2.imdecode(data, -1)
                    # cv2.imshow("window", dst)
                    # cv2.waitKey(0)
                    cv2.imwrite(os.path.join(folder, folder2, "L{0}_VX{1:04d}_VY{2:04d}_{3}.png"
                                             .format(top_down, x, y, i)), dst)

                json_open.close()
                f.close()
                print('{} ended'.format(folder2))
