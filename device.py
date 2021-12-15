import cv2
import numpy as np
import sys
import os

imgs = list()
msks = list()

file_dir = 'data/'
src_dir = 'src/'
mask_dir = 'mask/'

file_src= '20200218_102324_0_0_0403_0681_src.png'
file_mask= '20200218_102324_0_0_0403_0681_mask.png'
file_dst = '20210624.png'
print(os.path.exists(file_dir+src_dir+file_src))
print(os.path.exists(file_dir+mask_dir+file_mask))

img_src = cv2.imread(file_dir+src_dir+file_src,1) #入力画像の読み込み（カラー）
#img_src2 = cv2.imread(file_dir+src_dir+file_src,0) #入力画像の読み込む（グレー）

img_msk = cv2.imread(file_dir+mask_dir+file_mask,1) #（カラー）
#img_msk2 = cv2.imread(file_dir+mask_dir+file_mask,0)　#（グレー）


imgs.append(img_src)
msks.append(img_msk)

# #  ここに核となる処理を記述する  # #

element4 = np.array([[0,1,0],[1,1,1],[0,1,0]],np.uint8) #4近傍
element8 = np.array([[1,1,1],[1,1,1],[1,1,1]],np.uint8) #8近傍

##   回数   ##
su = 20
#roop = su+3


##  段階的ブラー処理  ##

for j in range(0,1,1):
    
    mask = cv2.cvtColor(msks[j],cv2.COLOR_RGB2GRAY)
    mask = cv2.threshold(mask, 220, 255,cv2.THRESH_BINARY)[1]
    img_blur = cv2.cvtColor(imgs[j],cv2.COLOR_RGB2GRAY)

    msknot = cv2.bitwise_not(mask)
    mskn = cv2.dilate(msknot,element4,iterations =1)
    msknot = mskn


    for i in range(0,su,1):

        mskn = cv2.erode(msknot,element4,iterations =1)
        msknot = mskn
        #cv2.imshow('erode',mskn)
        #cv2.waitKey(0)

        mask = cv2.bitwise_not(msknot)
        #cv2.imshow('mask',mask)
        #cv2.waitKey(0)


        ###############################
        img_msk0 = msknot

        img_msk1 = cv2.erode(img_msk0,element4,iterations = 1) 
        img_msk2 = cv2.erode(img_msk1,element4,iterations = 1)       
        msk = img_msk2

        if i == 12:
            mask_0 = mskn



        ##########################################

        if i <= 10:
            blur = cv2.blur(img_blur,(11,11))
            #cv2.imshow('blur',blur)
            #cv2.waitKey(0)
        else:
            blur =cv2.blur(img_blur,(3,3))
            #cv2.imshow('blur',blur)
            #cv2.waitKey(0)

        device = cv2.bitwise_and(blur,mask)
        #cv2.imshow('device',device)
        #cv2.waitKey(0)

        ######################################

        grays = cv2.cvtColor(imgs[j],cv2.COLOR_RGB2GRAY)
        inside = cv2.bitwise_and(grays,mskn)
        #cv2.imshow('inside',inside)
        #cv2.waitKey(0)

        dst = cv2.bitwise_or(device,inside)
        img_blur = dst
        #cv2.imshow('dst',dst)
        #cv2.waitKey(0)
    

cv2.imwrite('403.png',dst)

msk = cv2.bitwise_not(msk)

res = cv2.bitwise_and(msk,mask_0)
cv2.imwrite('res.png',res)

kekka =  cv2.bitwise_and(dst,res)
cv2.imwrite('kekka.png',kekka)

#############################


def keypoint(file):
    detector = cv2.AKAZE_create(threshold = 0.0001)  #強度を入れる
    gray = cv2.imread(file, cv2.IMREAD_GRAYSCALE)
    if gray is not None:
        keypoints = detector.detect(gray)
        # keypoints, descriptions = detector.detectAndCompute(gray, None)
        # print(len(descriptions))
        # print(len(descriptions[0]))
        # for d in descriptions[:10]:
        #     print("(%s, ..., %s)" % (", ".join(map(lambda x: "%.2f" % x, d[:4])), "%.2f" % d[-1]))
        #return plot_keypoints(cv2.imread(file, cv2.IMREAD_UNCHANGED), keypoints)
        return plot_key(cv2.imread(file, cv2.IMREAD_UNCHANGED),keypoints,mask)
    else:
        print("ERROR: file not found or not a image: %s" % file)
        return None



def plot_keypoints(image, keypoints):
    for keypoint in keypoints:
        x, y = keypoint.pt
        f.write(str(x) + ',' + str(y) + '\n')
        f.flush()
        cv2.circle(image, (int(x), int(y)), 5, (255, 0, 0), 1, 16)
    return image




def plot_key(image, keypoints, mask):

    if len(mask.shape) == 3 and mask.shape[2] == 3:
        # now mask shape (h, w, 3)
        mask = cv2.cvtColor(mask,cv2.COLOR_BGR2GRAY)
        # now mask shape (h, w)

    elif len(mask.shape) == 3:
        h, w, c = mask.shape
        # now mask shape (h, w, 1)
        mask = mask.reshape([h, w])
        # now mask shape (h, w)

    feature = 0

    for keypoint in keypoints:
        x, y = keypoint.pt
        if mask[int(y), int(x)] == 255:
            feature += 1
            cv2.circle(image, (int(x), int(y)), 3, (0, 255, 0), -1, 16)
        f.write(str(x) + ',' + str(y) + '\n')
        f.flush()
        cv2.circle(image, (int(x), int(y)), 5, (255, 0, 0), 1, 16)
    print(f"all feature {len(keypoints)}, on white feature {feature}")
    return image



if __name__ == "__main__":
    f=open('ten.csv','w')
    file = sys.argv[1]
    result = keypoint(file)
    if result is not None:
        basename, ext = os.path.splitext(file)
        cv2.imwrite(basename + "_device" + ext, result)
    f.close()
        
        

###############################################
