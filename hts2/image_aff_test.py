import cv2

path_img = 'B:/data/powerpoint/JPS2023/slide/fig/0-6.bmp'
write_path = 'B:/data/powerpoint/JPS2023/slide/fig/0-6_yfilp.bmp'
img = cv2.imread(path_img, 0)

img_flip_up = cv2.flip(img, 0)
cv2.imwrite(write_path, img_flip_up)
