import cv2
import numpy as np
import json
import sys
import os
import yaml

basepath = 'R:\\minami\\20221102_zabuton'
mode = 0  # 0:最後だけ、1:全画像 2:最初の画像

image = 'IMAGE00_AREA-1'

for n_t in range(1, 2):
    for n_m in range(1, 2):
        for n_v in range(1, 2):
            type = 'type{}'.format(n_t)
            module = 'Module{}'.format(n_m)
            version = 'ver-{}'.format(n_v)
            area = 'E'
            areapath = os.path.join(basepath, type, module, version, area)
            if os.path.exists(areapath)==False:
                continue
            os.chdir(areapath)
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

            os.makedirs(folder, exist_ok=True)

            x_size = param['Area'][0]['NViewX']  # x方向の大きさ
            y_size = param["Area"][0]["NViewY"]  # y方向の大きさ
            layer = param["Area"][0]["NLayer"]
            npicture = param["NPictures"]
            plate_sum = layer * x_size * y_size
            print(plate_sum)

            n = 0
            m = 0
            for y in range(0, y_size):
                for top_down in range(0, layer):
                    for x in range(0, x_size):
                        json_open = open('V{0:08d}_L{3:d}_VX{1:04d}_VY{2:04d}_0_{4:03d}.json'.format(n, x, y, top_down, npicture), 'r')
                        f = open("V{0:08d}_L{3:d}_VX{1:04d}_VY{2:04d}_0_{4:03d}.spng".format(n, x, y, top_down, npicture), "rb")
                        json_load = json.load(json_open)
                        print(n)
                        n += 1

                        folder2 = 'L{0}_VX{1:04}_VY{2:04}'.format(top_down, x, y)
                        if mode == 1:
                            os.makedirs(os.path.join(folder, folder2), exist_ok=True)

                        for i in range(0, len(json_load['Images'])):
                            filename = json_load['Images'][i]['Path']
                            filename_split = filename.split('&')
                            filesize = int(filename_split[-1])
                            data = np.fromfile(f, np.uint8, filesize, "", 8)
                            dst = cv2.imdecode(data, -1)
                            # cv2.imshow("window", dst)
                            # cv2.waitKey(0)
                            if mode == 0:
                                if i == len(json_load['Images']) - 1:
                                    if x == 0 and y == 0:
                                        cv2.imwrite(
                                            os.path.join(folder, "L{0}_VX{1:04d}_VY{2:04d}_{3}_{4}.png"
                                                         .format(top_down, x, y, i, m)), dst)
                                        m += 1
                                    else:
                                        cv2.imwrite(os.path.join(folder, "L{0}_VX{1:04d}_VY{2:04d}_{3}.png"
                                                                 .format(top_down, x, y, i)), dst)
                            elif mode == 1:
                                if x == 0 and y == 0:
                                    cv2.imwrite(os.path.join(folder, folder2, "L{0}_VX{1:04d}_VY{2:04d}_{3}_{4}.png"
                                                             .format(top_down, x, y, i, m)), dst)
                                else:
                                    cv2.imwrite(os.path.join(folder, folder2, "L{0}_VX{1:04d}_VY{2:04d}_{3}.png"
                                                             .format(top_down, x, y, i)), dst)

                            elif mode == 2:
                                if i == 0:
                                    cv2.imwrite(os.path.join(folder, "L{0}_VX{1:04d}_VY{2:04d}_{3}.png"
                                                             .format(top_down, x, y, i)), dst)

                        json_open.close()
                        f.close()
                        print('{} ended'.format(folder2))

                    json_open = open(
                        'V{0:08d}_L{3:d}_VX{1:04d}_VY{2:04d}_0_{4:03d}.json'.format(n, 0, 0, top_down, npicture),
                        'r')
                    f = open(
                        "V{0:08d}_L{3:d}_VX{1:04d}_VY{2:04d}_0_{4:03d}.spng".format(n, 0, 0, top_down, npicture),
                        "rb")
                    json_load = json.load(json_open)
                    print(n)
                    n += 1


                    folder2 = 'L{0}_VX{1:04}_VY{2:04}_{3}'.format(top_down, 0, 0, m)
                    if mode == 1:
                        os.makedirs(os.path.join(folder, folder2), exist_ok=True)

                    for i in range(0, len(json_load['Images'])):
                        filename = json_load['Images'][i]['Path']
                        filename_split = filename.split('&')
                        filesize = int(filename_split[-1])
                        data = np.fromfile(f, np.uint8, filesize, "", 8)
                        dst = cv2.imdecode(data, -1)
                        # cv2.imshow("window", dst)
                        # cv2.waitKey(0)
                        if mode == 1:
                            cv2.imwrite(os.path.join(folder, folder2, "L{0}_VX{1:04d}_VY{2:04d}_{3}.png"
                                                     .format(top_down, 0, 0, i)), dst)
                        if mode == 0:
                            if i == len(json_load['Images']) - 1:
                                cv2.imwrite(os.path.join(folder, "L{0}_VX{1:04d}_VY{2:04d}_{3}_{4}.png"
                                                         .format(top_down, 0, 0, i, m)), dst)

                    m += 1
                    json_open.close()
                    f.close()
                    print('{} ended'.format(folder2))
