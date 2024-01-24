import os.path

import cv2

img1_path = 'Q:/minami/20231204_fakeimg/p-0.0482-z0.404_dilate/IMAGE00_AREA-1/png/L0_VX0000_VY0000/L0_VX0000_VY0000_0.png'
img2_path = 'Q:/minami/20231204_fakeimg/p-0.0482-z0.404_dilate/IMAGE00_AREA-1/png/L0_VX0000_VY0000/L0_VX0000_VY0000_1.png'
out_path = 'B:/data/powerpoint/HTS2_data/4master_theisis/fake_img'

img1_gray = cv2.imread(img1_path, 0)
img2_gray = cv2.imread(img2_path, 0)
img1 = cv2.imread(img1_path)
img2 = cv2.imread(img2_path)
img_and = cv2.bitwise_and(img1_gray, img2_gray)
print(len(img_and), len(img_and[0]))
color = [0, 255, 51]
for y in range(len(img_and)):
    for x in range(len(img_and[0])):
        if not img_and[y][x] == 255:
            continue
        img1[y][x] = color
        # print(img1[y][x])
        img2[y][x] = color
    print('{} / {} eneded'.format(y, len(img_and)))

# img1[0] = img1[0] * 0
# img1[1] = img1[1] * 0
# img1 = img1 * 0
# cv2.imshow('test', img1[1000:1010, 600:610])
# cv2.waitKey(0)
# print(img1[1000:1010, 600:610])
cv2.imwrite(os.path.join(out_path, 'test1.png'), cv2.resize(img1[700:1000, 700:1000], None, fx=3, fy=3, interpolation=cv2.INTER_NEAREST))
cv2.imwrite(os.path.join(out_path, 'test2.png'), cv2.resize(img2[700:1000, 700:1000], None, fx=3, fy=3, interpolation=cv2.INTER_NEAREST))
