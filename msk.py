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

img_src = cv2.imread(file_dir+src_dir+file_src,1) #入力画像の読み込み（カラー）
img_msk = cv2.imread(file_dir+mask_dir+file_mask,1)
img_mskn = cv2.bitwise_not(img_msk) #マスク画像反転
# img_src = cv2.imread(file_src,0) #入力画像の読み込み（グレースカラー）

#cv2.namedWindow('src')
#cv2.namedWindow('dst')

#ここに核となる処理を記述する
img_dst = cv2.bitwise_and(img_src,img_mskn)

#cv2.imshow('src',img_src) #入力画像を表示
#cv2.imshow('dst',img_dst) #出力画像の表示
#cv2.waitKey(-1) #キー入力待ち
cv2.imwrite('msked1.png',img_dst) #処理結果の保存
cv2.destroyAllWindows()

