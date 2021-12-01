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


#cv2.namedWindow('src')
#cv2.namedWindow('dst')

#ここに核となる処理を記述する
element4 = np.array([[0,1,0],[1,1,1],[0,1,0]],np.uint8) #4近傍
element8 = np.array([[1,1,1],[1,1,1],[1,1,1]],np.uint8) #8近傍

img_msked = cv2.dilate(img_msk,element8,iterations = 1) #膨張処理
img_mskned = cv2.erode(img_mskn,element8,iterations = 1 ) #収縮処理
img_d1 = cv2.bitwise_and(img_src,img_msked) #機器のみ
img_d2 = cv2.bitwise_and(img_src,img_mskned) #機器いない
img_dst = cv2.blur(img_d1,(5,5)) #ぼかし処理
img_dst2 = cv2.bitwise_or(img_dst,img_d2) #合成
#cv2.imshow('src',img_src) #入力画像を表示
#cv2.imshow('dst',img_dst) #出力画像の表示
#cv2.waitKey(0) #キー入力待ち
cv2.imwrite('0703-1.png',img_dst2) #処理結果の保存

img_msked2 = cv2.dilate(img_msked,element8,iterations = 1) #膨張処理
img_mskned2 = cv2.erode(img_mskned,element8,iterations = 1 ) #収縮処理
img_d12 = cv2.bitwise_and(img_src,img_msked2) #機器のみ
img_d22 = cv2.bitwise_and(img_src,img_mskned2) #機器いない
img_dst12 = cv2.blur(img_d12,(5,5)) #ぼかし処理
img_dst22 = cv2.bitwise_or(img_dst12,img_d22) #合成
cv2.imwrite('0703-2.png',img_dst22)


#img_msked3 = cv2.dilate(img_msked2,element8,iterations = 1)
img_mskned3 = cv2.erode(img_mskned2,element8,iterations = 1 )
#img_d13 = cv2.bitwise_and(img_src,img_msked3)
img_d23 = cv2.bitwise_and(img_src,img_mskned3) 
#img_dst13 = cv2.blur(img_d13,(5,5))
img_dst23 = cv2.bitwise_or(img_dst12,img_d23)
cv2.imwrite('0703-3.png',img_dst23)

#cv2.destoroyAllWindows()


