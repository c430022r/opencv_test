import cv2
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

msk = list()
blur = list()
img = list()
mskn = list()
msked = list()
dst = list()

su = 8   #回数

img_msk0 = img_msk
img_blur0 =img_src

# 膨張処理　（白の部分が増える）
for i in range(0,su,1):
    img_msk1 = cv2.dilate(img_msk0,element8,iterations = 1) 
    img_msk2 = cv2.dilate(img_msk1,element8,iterations = 1)
    img_msk0 = cv2.dilate(img_msk2,element8,iterations = 1)
    msk.append(img_msk0)


#元画像のブラー処理（ぼかし）
for j in range(0,su,1):
    img_blur1 = cv2.blur(img_blur0,(3,3))
    blur.append(img_blur1)
    img_blur0 = img_blur1


# 膨張処理マスク画像+元画像ブラーの合成 ・・・△
# ブラー処理「弱」+　膨張処理「強」
for i in range(0,su,1):
    img.append(cv2.bitwise_and(blur[i],msk[4-i]))

#膨張処理マスク画像の反転・・・①
for j in range(0,su,1):
    mskn.append(cv2.bitwise_not(msk[4-j]))


# 元画像と①の合成・・・②
# ②と△の合成　
msked.append(cv2.bitwise_and(img_src,mskn[0]))
dst.append(cv2.bitwise_or(img[0],msked[0]))

for i in range(1,su,1):
   msked.append(cv2.bitwise_and(dst[i-1],mskn[i]))
   dst.append(cv2.bitwise_or(img[i],msked[i]))



#処理結果の保存
cv2.imwrite('last.png',dst[su-1])
