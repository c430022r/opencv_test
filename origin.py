import cv2
import numpy as np
import sys
import os
import glob


file_dir = 'data/'
src_dir = 'src/'
mask_dir = 'mask/'

file_src= '20200218_102324_0_0_0005_0681_src.png'
file_mask= '20200218_102324_0_0_0005_0681_mask.png'
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


#  回数

su = 20
#roop = su+3

img_blur = img_src
mask = img_msk

for i in range(0,su,1):

    msknot = cv2.bitwise_not(mask)
    #cv2.imshow('hannten',msknot)
    #cv2.waitKey(0)

    mskn = cv2.erode(msknot,element8,iterations =1)
    msknot = mskn
    #cv2.imshow('erode',mskn)
    #cv2.waitKey(0)

    mask = cv2.bitwise_not(msknot)
    #cv2.imshow('mask',mask)
    #cv2.waitKey(0)
    

    ##########################################


    blur = cv2.blur(img_blur,(su-i,su-i))
    #cv2.imshow('blur',blur)
    #cv2.waitKey(0)

    device = cv2.bitwise_and(blur,mask)
    #cv2.imshow('device',device)
    #cv2.waitKey(0)

    ######################################
    
    inside = cv2.bitwise_and(img_src,mskn)
    #cv2.imshow('inside',inside)
    #cv2.waitKey(0)
    
    dst = cv2.bitwise_or(device,inside)
    img_blur = dst
    #cv2.imshow('dst',dst)
    #cv2.waitKey(0)



