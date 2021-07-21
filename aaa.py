import cv2
import math 
import numpy as np
import os

file_dir = 'data/'
src_dir = 'src/'
mask_dir = 'mask/'

file_src= '20200218_102324_0_0_0001_0681_src.png'
file_mask= '20200218_102324_0_0_0001_0681_mask.png'
file_dst = '20210624.png'
print(os.path.exists(file_dir+src_dir+file_src))
print(os.path.exists(file_dir+mask_dir+file_mask))

image_list = list()
img_src1 = cv2.imread(file_dir+src_dir+file_src,1) #入力画像の読み込み（カラー）
#img_src2 = cv2.imread(file_dir+src_dir+file_src,0) #入力画像の読み込む（グレー）


#元画像のブラー処理（ぼかし）

img_b1 = cv2.blur(img_src1,(5,5))
img_b2 = cv2.blur(img_b1,(5,5))
img_b3 = cv2.blur(img_b2,(5,5))
img_b4 = cv2.blur(img_b3,(5,5))
img_b5 = cv2.blur(img_b4,(5,5))

cv2.imwrite('1.png',img_b1) #処理結果の保存
cv2.imwrite('2.png',img_b2)
cv2.imwrite('3.png',img_b3)
cv2.imwrite('4.png',img_b4)
cv2.imwrite('5.png',img_b5)


