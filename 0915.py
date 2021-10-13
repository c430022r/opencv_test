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


msk = list()
blur = list()
img = list()
mskn = list()
msked = list()
dst = list()

su = 25  #回数
han = su//2

img_msk0 = img_msk
img_blur0 =img_src

element4 = np.array([[0,1,0],[1,1,1],[0,1,0]],np.uint8) #4近傍

# 膨張処理　（白の部分が増える）
for i in range(0,su,1):
    img_msk1 = cv2.dilate(img_msk0,element4,iterations = 1) 
    img_msk2 = cv2.dilate(img_msk1,element4,iterations = 1)
    img_msk0 = cv2.dilate(img_msk2,element4,iterations = 1)
    msk.append(img_msk0)


#元画像のブラー処理（ぼかし）

for j in range(0,su,1):
    img_blur1 = cv2.blur(img_blur0,(18,18))
    blur.append(img_blur1)
    img_blur0 = img_blur1
    
    
# 膨張処理マスク画像+元画像ブラーの合成 

a = su-1

for i in range(0,su,1):
    img.append(cv2.bitwise_and(blur[i],msk[a-i]))    


cv2.imwrite('img1.png',img[1])
cv2.imwrite('img2.png',img[2])
cv2.imwrite('img3.png',img[3])
cv2.imwrite('img4.png',img[4])
cv2.imwrite('img5.png',img[5])
cv2.imwrite('img6.png',img[6])
cv2.imwrite('img7.png',img[7])
cv2.imwrite('img8.png',img[8])
cv2.imwrite('img9.png',img[9])
cv2.imwrite('img10.png',img[10])
cv2.imwrite('img11.png',img[11])




