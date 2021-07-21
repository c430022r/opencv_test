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

img_msk = cv2.imread(file_dir+mask_dir+file_mask,1) #（カラー）
#img_msk2 = cv2.imread(file_dir+mask_dir+file_mask,0)　#（グレー）



#ここに核となる処理を記述する
element4 = np.array([[0,1,0],[1,1,1],[0,1,0]],np.uint8) #4近傍
element8 = np.array([[1,1,1],[1,1,1],[1,1,1]],np.uint8) #8近傍

#元画像のブラー処理（ぼかし）
img_b1 = cv2.blur(img_src1,(5,5))
img_b2 = cv2.blur(img_b1,(5,5))
img_b3 = cv2.blur(img_b2,(5,5))
img_b4 = cv2.blur(img_b3,(5,5))
img_b5 = cv2.blur(img_b4,(5,5))

img_msk1 = cv2.dilate(img_msk,element8,iterations = 1) #膨張処理　（白の部分が増える）
img_msk2 = cv2.dilate(img_msk1,element8,iterations = 1)
img_msk3 = cv2.dilate(img_msk2,element8,iterations = 1)

img_msk4 = cv2.dilate(img_msk3,element8,iterations = 1)
img_msk5 = cv2.dilate(img_msk4,element8,iterations = 1)
img_msk6 = cv2.dilate(img_msk5,element8,iterations = 1)

img_msk7 = cv2.dilate(img_msk6,element8,iterations = 1)
img_msk8 = cv2.dilate(img_msk7,element8,iterations = 1)
img_msk9 = cv2.dilate(img_msk8,element8,iterations = 1)

img_msk10 = cv2.dilate(img_msk9,element8,iterations = 1)
img_msk11 = cv2.dilate(img_msk10,element8,iterations = 1)
img_msk12 = cv2.dilate(img_msk11,element8,iterations = 1)

img_msk13 = cv2.dilate(img_msk12,element8,iterations = 1)
img_msk14 = cv2.dilate(img_msk13,element8,iterations = 1)
img_msk15 = cv2.dilate(img_msk14,element8,iterations = 1)


#img_dst2 = cv2.erode(img_mskn2,element8,iterations = 1)　#収縮処理　（黒の部分が増える）


img_img1 = cv2.bitwise_and(img_b1,img_msk15)
img_img2 = cv2.bitwise_and(img_b2,img_msk12)
img_img3 = cv2.bitwise_and(img_b3,img_msk9)
img_img4 = cv2.bitwise_and(img_b4,img_msk6)
img_img5 = cv2.bitwise_and(img_b5,img_msk3)


img_msked5 = cv2.bitwise_or(img_src1,img_msk15)
img_dst1 = cv2.bitwise_and(img_msked5,img_img1)

img_msked4 = cv2.bitwise_or(img_dst1,img_msk12)
img_dst2 = cv2.bitwise_and(img_msked4,img_img2)

img_msked3 = cv2.bitwise_or(img_dst2,img_msk9)
img_dst3 = cv2.bitwise_and(img_msked3,img_img3)

img_msked2 = cv2.bitwise_or(img_dst3,img_msk6)
img_dst4 = cv2.bitwise_and(img_msked2,img_img4)

img_msked1 = cv2.bitwise_or(img_dst4,img_msk3)
img_dst5 = cv2.bitwise_and(img_msked1,img_img5)


cv2.imwrite('0715-1.png',img_dst1) #処理結果の保存
cv2.imwrite('0715-2.png',img_dst2)
cv2.imwrite('0715-3.png',img_dst3)
cv2.imwrite('0715-4.png',img_dst4)
cv2.imwrite('0715-5.png',img_dst5)

#cv2.destoroyAllWindows()
