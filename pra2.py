import cv2
import math 
import numpy as np

file_src= 'msk.png'
file_dst = 'msked.png'

img_src = cv2.imread(file_src,1) #入力画像の読み込み（カラー）
# img_src = cv2.imread(file_src,0) #入力画像の読み込む（グレースカラー）

cv2.namedWindow('src')
cv2.namedWindow('dst')

#ここに核となる処理を記述する
img_tmp = cv2.Sobel(img_src,cv2.CV_32F,1,0)
img_dst = cv2.convertScaleAbs(img_tmp)

cv2.imshow('src',img_src) #入力画像を表示
cv2.imshow('dst',img_dst) #出力画像の表示
cv2.imwrite('masked.png',img_dst) #処理結果の保存
cv2.waitKey(0) #キー入力待ち
cv2.destoroyAllWindows()


