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
mask = list()
blur = list()
img = list()
mskn = list()
maskn = list()
msked = list()
dst = list()
abc = list()
xyz = list()
hako = list()
hakod = list()

su = 20  #回数
han = su//2



#マスク画像の反転

img_msk0 = cv2.bitwise_not(img_msk)

# 収縮処理　（黒の部分が増える）・・・①

msk0 = cv2.dilate(img_msk0,element8,iterations = 1) 

for i in range(0,su,1):
    img_msk1 = cv2.erode(img_msk0,element8,iterations = 1)     
    msk.append(img_msk1)
    img_msk0 = img_msk1

    #cv2.imwrite('msk.png',msk[10])
    
for i in range(0,su,1):
    img_msk1 = cv2.erode(img_msk0,element8,iterations = 1) 
    img_msk2 = cv2.erode(img_msk1,element8,iterations = 1)       
    img_msk0 = img_msk2
    mask.append(img_msk2)
    
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
  
for j in range(0,su,1):
    maskn.append(cv2.bitwise_not(mask[a-j]))
    
    
# 収縮処理「強」+ ブラー処理「弱」
# 収縮処理マスク画像 + 元画像ブラーの合成 ・・・④ 

for i in range(0,su,1):
    img.append(cv2.bitwise_and(mskn[a-i],blur[i]))

cv2.imwrite('img.png',img[5])


# 元画像とマスク画像の合成　・・・⑤
msked.append(cv2.bitwise_and(img_src,msk[0]))

cv2.imwrite('msked.png',msked[0])

# ぼかし機器のみの画像④　+　元画像機器なしの画像⑤
dst.append(cv2.bitwise_or(img[0],msked[0]))

cv2.imwrite('dst.png',dst[0])

for i in range(1,su,1):
   msked.append(cv2.bitwise_and(dst[i-1],msk[i]))
   dst.append(cv2.bitwise_or(img[i],msked[i]))

cv2.imwrite('a.png',dst[a])


# 箱谷のやり方  
hako.append(cv2.bitwise_and(blur[a-1],mskn[0]))
cv2.imwrite('hako.png',hako[0])
hakod.append(cv2.bitwise_or(hako[0],msked[0]))

cv2.imwrite('hakod.png',hakod[0])


# 境界上の特徴点調べ
abc.append(cv2.bitwise_and(msk0,dst[a-1]))
abc.append(cv2.bitwise_and(maskn[0],dst[a-1]))
   
xyz.append(cv2.bitwise_and(abc[0],abc[1]))
cv2.imwrite('1010.png',xyz[0])


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
        return plot_keypoints(cv2.imread(file, cv2.IMREAD_UNCHANGED), keypoints)
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

if __name__ == "__main__":
    f=open('ten.csv','w')
    file = sys.argv[1]
    result = keypoint(file)
    if result is not None:
        basename, ext = os.path.splitext(file)
        cv2.imwrite(basename + "_fp" + ext, result)
    f.close()
        
        



















