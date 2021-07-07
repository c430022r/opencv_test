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


img_src1 = cv2.imread(file_dir+src_dir+file_src,1) #入力画像の読み込み（カラー）
#img_src2 = cv2.imread(file_dir+src_dir+file_src,0) #入力画像の読み込む（グレー）

img_msk = cv2.imread(file_dir+mask_dir+file_mask,1)　#（カラー）
#img_msk2 = cv2.imread(file_dir+mask_dir+file_mask,0)　#（グレー）



#ここに核となる処理を記述する
element4 = np.array([[0,1,0],[1,1,1],[0,1,0]],np.uint8) #4近傍
element8 = np.array([[1,1,1],[1,1,1],[1,1,1]],np.uint8) #8近傍

#元画像のブラー処理（ぼかし）
img_b1 = cv2.blur(img_src,(5,5))
img_b1 = cv2.blur(img_src,(5,5))
img_b1 = cv2.blur(img_src,(5,5))
img_b1 = cv2.blur(img_src,(5,5))
img_b1 = cv2.blur(img_src,(5,5))


img_dst = cv2.dilate(img_msk2,element8,iterations = 1) #膨張処理　（白の部分が増える）
img_dst2 = cv2.erode(img_mskn2,element8,iterations = 1)　#収縮処理　（黒の部分が増える）



#img_dst2 = cv2.blur(img_d1,(5,5))

#img_dst3= cv2.erode(img_dst2,element4,iterations = 1 )

#img_dst4 = cv2.bitwise_or(img_dst3,img_dst)
#img_dst5 = cv2.merge((img_dst4,img_dst4,img_dst4))

#cv2.imshow('src',img_msk2) #入力画像を表示
#cv2.imshow('dst',img_dst) #出力画像の表示
#cv2.waitKey(0) #キー入力待ち

cv2.imwrite('0707-1.png',img_dst) #処理結果の保存
cv2.imwrite('0707-2.png',img_dst2)
#cv2.destoroyAllWindows()


