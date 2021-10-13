import cv2
import numpy as np
import sys
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

msk = list()
blur = list()
img = list()
mskn = list()
msked = list()
dst = list()

su = 20  #回数
han = su//2



#マスク画像の反転

mskn.append(cv2.bitwise_not(img_msk))


# 収縮処理　（黒の部分が増える）・・・①

img_msk0 = mskn[0] 
msk0 = cv2.dilate(img_msk0,element8,iterations = 1) 


for i in range(0,su,1):
    img_msk1 = cv2.erode(img_msk0,element8,iterations = 1) 
    msk.append(img_msk1)
    img_msk0 = img_msk1
    
#元画像のブラー処理（ぼかし）・・・②

img_blur0 =img_src

for j in range(0,han,1):
    img_blur1 = cv2.blur(img_blur0,(5,5))
    blur.append(img_blur1)
    img_blur0 = img_blur1

for j in range(han,su,1):
    img_blur1 = cv2.blur(img_blur0,(15,15))
    blur.append(img_blur1)
    img_blur0 = img_blur1


#収縮処理マスク画像の反転・・・③

a = su-1

for j in range(0,su,1):
    mskn.append(cv2.bitwise_not(msk[a-j]))
  

# 収縮処理「強」+ ブラー処理「弱」
# 収縮処理マスク画像 + 元画像ブラーの合成 ・・・④ 

img.append(cv2.bitwise_and(msk0,blur[su-1]))
img.append(cv2.bitwise_and(mskn[a-5],blur[su-1]))

cv2.imwrite('img1.png',img[0])
cv2.imwrite('img2.png',img[1])


msked.append(cv2.bitwise_and(img[0],img[1]))
cv2.imwrite('msked.png',msked[0])



























