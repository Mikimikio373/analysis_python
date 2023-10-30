import cv2

path = "Q:/minami/graine_u4/PL088/IMAGE00_AREA-1/png/L0_VX0000_VY0000/L0_VX0000_VY0000_11.png"

img = cv2.imread(path, 0)
img_cut = img[200:400, 200:400]
out = "Q:/minami/graine_u4/PL088/IMAGE00_AREA-1/png/L0_VX0000_VY0000/L0_VX0000_VY0000_11_cut1.png"
print(out)
cv2.imwrite(out, img_cut)

img_cut2 = img[200:400, 240:440]
out = "Q:/minami/graine_u4/PL088/IMAGE00_AREA-1/png/L0_VX0000_VY0000/L0_VX0000_VY0000_11_cut2.png"
cv2.imwrite(out, img_cut2)