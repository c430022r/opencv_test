import cv2
import numpy as np
import glob

files = glob.glob("./data/shiro/image_raw/*.jpg")

imgs = list()
msks = list()
count = 0

files = sorted(files)
for file in files:
    img = cv2.imread(file)   #cv2.imread(    , 1) <--- color
    width = img.shape[1]     #左右の分割
    left = img[:,0:width//2]
    right = img[:,width//2:]
    left = left[35:1044,165:795]
    right = right[35:1044,165:795]
    imgs.append(left)    #imgs[]  <---  偶数
    imgs.append(right)   #imgs[]  <---  奇数
    count+=2
    break
    #print(file)

mskfiles = glob.glob("./data/shiro/mask/*.png")

mskfiles = sorted(mskfiles)
for file in mskfiles:
    img = cv2.imread(file)
    width = img.shape[1]
    left = img[:,0:width//2]
    right = img[:,width//2:]
    msks.append(left)
    msks.append(right)
    break
    #print(file)


# #  ここに核となる処理を記述する  # #
element4 = np.array([[0,1,0],[1,1,1],[0,1,0]],np.uint8) #4近傍
element8 = np.array([[1,1,1],[1,1,1],[1,1,1]],np.uint8) #8近傍

mskns = list()
blurs = list()
masks = list()
image = list()
msked = list()
dst = list()


su = 16  #回数
han = su//2
a = su-1

#マスク画像の反転

for j in range(0,count,1):

    gray = cv2.cvtColor(msks[j],cv2.COLOR_RGB2GRAY)
    img_msk0 = cv2.bitwise_not(gray)

    #img_msk0 = cv2.bitwise_not(msks[j])   #<---color

    #img_mask = cv2.bitwise_not(img_msk)
    
    # 収縮処理　（黒の部分が増える）・・・①
    for i in range(0,su,1):

        img_msk1 = cv2.erode(img_msk0,element8,iterations = 1) 
        mskns.append(img_msk1)
        img_msk0 = img_msk1
        
        #cv2.imwrite('msk.png',msk[10])  

    #img_msk0 = cv2.bitwise_not(img_msk)
    #img_msk1 = cv2.erode(img_msk0,element8,iterations = 1) 
    #mask.append(cv2.bitwise_not(img_msk1))

    #for i in range(1,su,1):
        #img_msk1 = cv2.erode(img_msk0,element8,iterations = 1) 
        #img_msk2 = cv2.erode(img_msk1,element4,iterations = 1)       
        #img_msk0 = img_msk2
        #mask.append(cv2.bitwise_not(img_msk2))

    #元画像のブラー処理（ぼかし）・・・②
    gray = cv2.cvtColor(imgs[j],cv2.COLOR_RGB2GRAY)
    img_blur0 = gray

    #img_blur0 = imgs[j]  #<--color

    for i in range(0,han,1):
        img_blur1 = cv2.blur(img_blur0,(7,7))
        img_blur2 = cv2.blur(img_blur1,(7,7))
        blurs.append(img_blur2)
        img_blur0 = img_blur2

    for i in range(han,su,1):
        img_blur1 = cv2.blur(img_blur0,(21,21))
        img_blur2 = cv2.blur(img_blur1,(21,21))
        blurs.append(img_blur2)
        img_blur0 = img_blur2

    #収縮処理マスク画像の反転・・・③
    for i in range(0,su,1):
        masks.append(cv2.bitwise_not(mskns[a-i]))
    
    # 収縮処理「強」+ ブラー処理「弱」
    # 収縮処理マスク画像 + 元画像ブラーの合成 ・・・④ 

    #print(masks[0].shape, blurs[0].shape)
    

    for i in range(0,su,1):
        #blur = cv2.cvtColor(blurs[a-i], cv2.COLOR_GRAY2BGR)
        #mask = np.reshape(masks[a-i], (masks[i].shape[0], masks[i].shape[1], 1))
        #mask = cv2.cvtColor(masks[a-i], cv2.COLOR_GRAY2BGR)
        image.append(cv2.bitwise_and(blurs[i], masks[a-i]))


    # 元画像とマスク画像の合成　・・・⑤
    gray = cv2.cvtColor(imgs[j],cv2.COLOR_RGB2GRAY)
    msked.append(cv2.bitwise_and(gray,mskns[0]))

    #msked.append(cv2.bitwise_and(imgs[j],mskns[0]))  #<---color

    # ぼかし機器のみの画像④　+　元画像機器なしの画像⑤
    dst.append(cv2.bitwise_or(image[0],msked[0]))

    for i in range(1,su,1):
        msked.append(cv2.bitwise_and(dst[i-1],mskns[i]))
        dst.append(cv2.bitwise_or(image[i],msked[i]))

    cv2.imwrite('pra.png',dst[a])

#res.append(cv2.bitwise_and(mask[16],msk[18]))
#cv2.imwrite('res.png',res[0])

#img0 = cv2.bitwise_and(res[0],dst[a])
#cv2.imwrite('kekka.png',img0)


#msk.append(cv2.dilate(img_mask,element8,iterations = 1)) 

#IMG.append(cv2.bitwise_and(mskn[a],blur[a]))
#hako.append(cv2.bitwise_and(img_src,msk[0]))
#hakoed.append(cv2.bitwise_or(IMG[0],hako[0]))
#cv2.imwrite('hako.png',hakoed[0])


#res.append(cv2.bitwise_and(mask[3],msk[su]))
#cv2.imwrite('mask.png',mask[0])
#cv2.imwrite('msk.png',msk[su])
#cv2.imwrite('res1.png',res[1])
#img1 = cv2.bitwise_and(res[1],hakoed[0])
#cv2.imwrite('kekka1.png',img1)

