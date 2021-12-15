import cv2
import numpy as np
import sys
import os

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

msk = list()
mskn = list()
msked = list()
blur = list()
img = list()
dst = list()

IMG = list()
hako = list()
hakoed = list()

mask = list() 
res = list()

su = 15  #回数
han = su//2
q = su//8

a = su-1


#マスク画像の反転

img_msk0 = cv2.bitwise_not(img_msk)
img_mask = cv2.bitwise_not(img_msk)

# 収縮処理　（黒の部分が増える）・・・①

for i in range(0,su,1):
    img_msk1 = cv2.erode(img_msk0,element8,iterations = 1) 
    msk.append(img_msk1)
    img_msk0 = img_msk1
    
    #cv2.imwrite('msk.png',msk[10])  

img_msk0 = cv2.bitwise_not(img_msk)
img_msk1 = cv2.erode(img_msk0,element4,iterations = 1) 
mask.append(cv2.bitwise_not(img_msk1))

for i in range(1,su,1):
    img_msk1 = cv2.erode(img_msk0,element8,iterations = 1) 
    img_msk2 = cv2.erode(img_msk1,element4,iterations = 1)       
    img_msk0 = img_msk2
    mask.append(cv2.bitwise_not(img_msk2))

#元画像のブラー処理（ぼかし）・・・②

img_blur0 =img_src

for j in range(0,han,1):
    img_blur1 = cv2.blur(img_blur0,(7,7))
    img_blur2 = cv2.blur(img_blur1,(7,7))
    blur.append(img_blur2)
    img_blur0 = img_blur2

for j in range(han,su,1):
    img_blur1 = cv2.blur(img_blur0,(19,19))
    img_blur2 = cv2.blur(img_blur1,(19,19))
    blur.append(img_blur2)
    img_blur0 = img_blur2


#収縮処理マスク画像の反転・・・③


for j in range(0,su,1):
    mskn.append(cv2.bitwise_not(msk[a-j]))
  

# 収縮処理「強」+ ブラー処理「弱」
# 収縮処理マスク画像 + 元画像ブラーの合成 ・・・④ 

for i in range(0,su,1):
    img.append(cv2.bitwise_and(mskn[a-i],blur[i]))


# 元画像とマスク画像の合成　・・・⑤
msked.append(cv2.bitwise_and(img_src,msk[0]))


# ぼかし機器のみの画像④　+　元画像機器なしの画像⑤
dst.append(cv2.bitwise_or(img[0],msked[0]))


for i in range(1,su,1):
   msked.append(cv2.bitwise_and(dst[i-1],msk[i]))
   dst.append(cv2.bitwise_or(img[i],msked[i]))
   
cv2.imwrite('a.png',dst[a])

res.append(cv2.bitwise_and(mask[10],msk[han+q]))
cv2.imwrite('res.png',res[0])

img0 = cv2.bitwise_and(res[0],dst[a])
cv2.imwrite('kekka.png',img0)


msk.append(cv2.dilate(img_mask,element8,iterations = 1)) 

IMG.append(cv2.bitwise_and(mskn[a],blur[a]))
hako.append(cv2.bitwise_and(img_src,msk[0]))
hakoed.append(cv2.bitwise_or(IMG[0],hako[0]))
cv2.imwrite('hako.png',hakoed[0])


res.append(cv2.bitwise_and(mask[3],msk[su]))
cv2.imwrite('mask.png',mask[0])
cv2.imwrite('msk.png',msk[su])
cv2.imwrite('res1.png',res[1])
img1 = cv2.bitwise_and(res[1],hakoed[0])
cv2.imwrite('kekka1.png',img1)


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
        return plot_key(cv2.imread(file, cv2.IMREAD_UNCHANGED),keypoints,res[1])
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

    if mask.shape[2] == 3:
        mask = cv2.cvtColor(mask,cv2.COLOR_BGR2GRAY)

    feature = 0

    for keypoint in keypoints:
        x, y = keypoint.pt
        if mask[int(y), int(x)] == 255:
            feature += 1
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
        cv2.imwrite(basename + "_fp" + ext, result)
    f.close()
        
        



















