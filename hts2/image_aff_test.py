import cv2

path_img = 'B:\\data\\powerpoint\\GRAINE_nagoya_local\\graine20230530\\fig\\test0-6_adjust.jpg'
write_path = 'B:\\data\\powerpoint\\GRAINE_nagoya_local\\graine20230530\\fig\\test0-6_adjust_flip.png'
img = cv2.imread(path_img, 0)

img_flip_up = cv2.flip(img, 0)
cv2.imwrite(write_path, img_flip_up)
