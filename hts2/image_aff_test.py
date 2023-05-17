import cv2

path_img = 'R:\\minami\\20230106_overrap\\0-9.jpg'
write_path = 'R:\\minami\\20230106_overrap\\0-9_flip.png'
img = cv2.imread(path_img, 0)

img_flip_up = cv2.flip(img, 0)
cv2.imwrite(write_path, img_flip_up)
