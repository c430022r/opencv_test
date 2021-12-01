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
#img_src2 = cv2.imread(file_dir+src_dir+file_src,0) #入力画像の読み込む（グレー）

img_msk = cv2.imread(file_dir+mask_dir+file_mask,1) #（カラー）
#img_msk2 = cv2.imread(file_dir+mask_dir+file_mask,0)　#（グレー）


# #  ここに核となる処理を記述する  # #

element4 = np.array([[0,1,0],[1,1,1],[0,1,0]],np.uint8) #4近傍
element8 = np.array([[1,1,1],[1,1,1],[1,1,1]],np.uint8) #8近傍

msk=[0,1,2,3,4]
blur=[0,1,2,3,4]
img=[0,1,2,3,4]
mskn=[0,1,2,3,4]
msked=[0,1,2,3,4]
dst=[0,1,2,3,4]

img_msk0 = img_msk
img_blur0 =img_src

# 膨張処理　（白の部分が増える）
for i in range(0,5,1):
    img_msk1 = cv2.dilate(img_msk0,element8,iterations = 1) 
    img_msk2 = cv2.dilate(img_msk1,element8,iterations = 1)
    img_msk0 = cv2.dilate(img_msk2,element8,iterations = 1)
    msk[i]=img_msk0


#元画像のブラー処理（ぼかし）
for j in range(0,5,1):
    img_blur1 = cv2.blur(img_blur0,(4,4))
    blur[j] = img_blur1
    img_blur0 = img_blur1


# 膨張処理マスク画像+元画像ブラーの合成 ・・・△
# ブラー処理「弱」+　膨張処理「強」
for i in range(0,5,1):
    img[i] = cv2.bitwise_and(blur[(i)],msk[4-i])


#膨張処理マスク画像の反転・・・①
for j in range(0,5,1):
    mskn[j] = cv2.bitwise_not(msk[4-j])


# 元画像と①の合成・・・②
# ②と△の合成　
msked[0] = cv2.bitwise_and(img_src,mskn[0])
dst[0] = cv2.bitwise_or(img[0],msked[0])

for i in range(1,5,1):
   msked[i] = cv2.bitwise_and(dst[i-1],mskn[i])
   dst[i] = cv2.bitwise_or(img[i],msked[i])


#処理結果の保存
cv2.imwrite('0721-0.png',dst[0])
cv2.imwrite('0721-1.png',dst[1]) 
cv2.imwrite('0721-2.png',dst[2])
cv2.imwrite('0721-3.png',dst[3])
cv2.imwrite('0721-4.png',dst[4])

#cv2.destoroyAllWindows()
