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

img_msk0 = img_msk
img_blur0 =img_src

# 膨張処理　（白の部分が増える）
for i in range(0,su,1):
    img_msk1 = cv2.dilate(img_msk0,element4,iterations = 1) 
    img_msk2 = cv2.dilate(img_msk1,element4,iterations = 1)
    img_msk0 = cv2.dilate(img_msk2,element4,iterations = 1)
    msk.append(img_msk0)



#元画像のブラー処理（ぼかし）
for j in range(0,han,1):
    img_blur1 = cv2.blur(img_blur0,(7,7))
    blur.append(img_blur1)
    img_blur0 = img_blur1

for j in range(han,su,1):
    img_blur1 = cv2.blur(img_blur0,(19,19))
    blur.append(img_blur1)
    img_blur0 = img_blur1



# 膨張処理マスク画像+元画像ブラーの合成 ・・・△
# ブラー処理「弱」+　膨張処理「強」

a = su-1

for i in range(0,su,1):
    img.append(cv2.bitwise_and(blur[i],msk[a-i]))

#膨張処理マスク画像の反転・・・①
for j in range(0,su,1):
    mskn.append(cv2.bitwise_not(msk[a-j]))


# 元画像と①の合成・・・②
# ②と△の合成　
msked.append(cv2.bitwise_and(img_src,mskn[0]))
dst.append(cv2.bitwise_or(img[0],msked[0]))

for i in range(1,su,1):
   msked.append(cv2.bitwise_and(dst[i-1],mskn[i]))
   dst.append(cv2.bitwise_or(img[i],msked[i]))

cv2.imwrite('20.png',dst[su-1])

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
        cv2.circle(image, (int(x), int(y)), 5, (255, 0, 0), 1, 16)
    return image

if __name__ == "__main__":
    file = sys.argv[1]
    result = keypoint(file)
    if result is not None:
        basename, ext = os.path.splitext(file)
        cv2.imwrite(basename + "_fp" + ext, result)
        
        



