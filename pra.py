import glob
import os
import cv2
import numpy as np

#file_dir = 'data/'
#src_dir = 'src/'
#mask_dir = 'mask/'

#file_src= '20200218_102324_0_0_0001_0681_src.png'
#file_mask= '20200218_102324_0_0_0001_0681_mask.png'
#file_dst = '20210624.png'


img_array = []
for filename in sorted(glob.glob("./data/*.png")):
    img = cv2.imread(filename)
    height, width, layers = img.shape
    size = (width, height)
    img_array.append(img)

name = 'proj.mp4'
out = cv2.VideoWriter(name, cv2.VideoWriter_fourcc(*'MP4V'), 5.0, size)

for i in range(len(img_array)*100):
    out.write(img_array[0])
out.release()