import cv2
import math 
import numpy as np

file_src= 'msk.png'
file_dst = 'msked.png'

img_src #前景画像
img_bkg #背景画像
img_dst #切り出した画像

img_src = cv2.imread(file_src,1) #入力画像の読み込み（カラー）
# img_src = cv2.imread(file_src,0) #入力画像の読み込む（グレースカラー）

cv2.namedWindow('src')
cv2.namedWindow('dst')

#ここに核となる処理を記述する

#背景画像との差分画像を計算
img_df = cv2.absdiff(img_src, img_bkg)
#差分画像の２値化
img_m = cv2.threshold(img_df, 50, 255, cv2.THRESH_BINARY)[1]
#膨張・収縮してマスク画像を生成
op = np.ones((3,3), np.uint8)
img_md = cv2_dilate(img_m, op, iterations = 4)
img_msk = cv2_erode(img_md, op, iterations = 4)
#マスク画像を使って対象を切り出す
img_dst = cv2_bitwise_and(img_src,img_msk) 

cv2.imshow('src',img_src) #入力画像を表示
cv2.imshow('dst',img_dst) #出力画像の表示
cv2.imwrite('msked1.png',img_dst) #処理結果の保存
cv2.waitKey(0) #キー入力待ち
cv2.destoroyAllWindows()


