from PIL import Image
import glob
import os

pngpath = 'Q:\\minami\\20220503_forGrainMaching05\\type1\Module1\\ver-1\E\IMAGE00_AREA-1\\png\\L0_VX0000_VY0001\\GrainMatching4vib\\plot'
os.chdir(pngpath)
current_path = os.getcwd()
print('path changed current path: ', current_path)

files = sorted(glob.glob('./*.png'))
print('sort ended')
images = list(map(lambda file: Image.open(file), files))
print('memory onboard')
print('make gif')
images[0].save('viv.gif', save_all=True, append_images=images[1:], duration=300, loop=0)

