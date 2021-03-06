import cv2
import numpy as np
import glob

files = glob.glob("./data/shiro/image_raw/*.jpg")

imgs = list()
msks = list()
count = 0

#img_array = []

name = 'project_1208.mp4'

files = sorted(files)
for file in files:
    img = cv2.imread(file)   #cv2.imread(    , 1) <--- color
    width = img.shape[1]     #左右の分割
    height = img.shape[0]
    size = (width, height)
    left = img[:,0:width//2]
    right = img[:,width//2:]
    left = left[35:1044,165:795]
    right = right[35:1044,165:795]
    imgs.append(left)    #imgs[]  <---  偶数
    imgs.append(right)   #imgs[]  <---  奇数
    #count+=1
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
    count+=2
    #print(file)


#width = imgs[0].shape[1]     #左右の分割
#height = imgs[0].shape[0]
size = (1260,1009)
out = cv2.VideoWriter(name, cv2.VideoWriter_fourcc(*'MP4V'), 30.0, size)
#print(size)

# #  ここに核となる処理を記述する  # #
element4 = np.array([[0,1,0],[1,1,1],[0,1,0]],np.uint8) #4近傍
element8 = np.array([[1,1,1],[1,1,1],[1,1,1]],np.uint8) #8近傍

mskns = list()
blurs = list()
masks = list()
image = list()
msked = list()
dst = list()
color = list()


su =  20 #回数
han = su//2
a = su-1


#マスク画像の反転
#print(count)

for j in range(0,count,1):
    #print(j)
    
    mskns.clear()
    blurs.clear()
    masks.clear()
    image.clear()
    msked.clear()
    dst.clear()
    

    gray = cv2.cvtColor(msks[j],cv2.COLOR_RGB2GRAY)
    img_msk0 = cv2.bitwise_not(gray)

    #img_msk0 = cv2.bitwise_not(msks[j])   #<---color

    #img_mask = cv2.bitwise_not(img_msk)
    
    # 収縮処理　（黒の部分が増える）・・・①
    for i in range(0,su,1):

        img_msk1 = cv2.erode(img_msk0,element8,iterations = 1)
        img_msk2 = cv2.erode(img_msk1,element8,iterations = 1)
        #img_msk3 = cv2.erode(img_msk2,element4,iterations = 1)  
        mskns.append(img_msk2)
        img_msk0 = img_msk2
        
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
    img_blur0  = cv2.cvtColor(imgs[j],cv2.COLOR_RGB2GRAY)
    

    #img_blur0 = imgs[j]  #<--color

    for i in range(0,5,1):
        img_blur1 = cv2.blur(img_blur0,(3,3))
        blurs.append(img_blur1)
        img_blur0 = img_blur1

    for i in range(5,10,1):
        img_blur1 = cv2.blur(img_blur0,(9,9))
        blurs.append(img_blur1)
        img_blur0 = img_blur1

    for i in range(10,su,1):
        img_blur1 = cv2.blur(img_blur0,(15,15))
        blurs.append(img_blur1)
        img_blur0 = img_blur1

    #収縮処理マスク画像の反転・・・③
    for i in range(0,su,1):
        masks.append(cv2.bitwise_not(mskns[i]))
    
    # 収縮処理「強」+ ブラー処理「弱」
    # 収縮処理マスク画像 + 元画像ブラーの合成 ・・・④ 

    #print(masks[0].shape, blurs[0].shape)
    

    for i in range(0,su,1):
        #blur = cv2.cvtColor(blurs[a-i], cv2.COLOR_GRAY2BGR)
        #mask = np.reshape(masks[a-i], (masks[i].shape[0], masks[i].shape[1], 1))
        #mask = cv2.cvtColor(masks[a-i], cv2.COLOR_GRAY2BGR)
        image.append(cv2.bitwise_and(blurs[a-i], masks[i]))
        #cv2.imshow('image', image[i])
        #cv2.waitKey(1)

    #cv2.imshow('image', image[0])
    #cv2.waitKey(1)
    # 元画像とマスク画像の合成　・・・⑤
    grays = cv2.cvtColor(imgs[j],cv2.COLOR_RGB2GRAY)
    msked.append(cv2.bitwise_and(grays,mskns[a]))
    
    #cv2.imshow('grays', grays)
    #cv2.waitKey(1)
    #cv2.imshow('msked', msked[0])
    #cv2.waitKey(1)

    #msked.append(cv2.bitwise_and(imgs[j],mskns[0]))  #<---color

    # ぼかし機器のみの画像④　+　元画像機器なしの画像⑤
    dst.append(cv2.bitwise_or(image[a],msked[0]))

    #cv2.imshow('dst', dst[0])
    #cv2.waitKey(1)

    for i in range(1,su,1):
        msked.append(cv2.bitwise_and(dst[i-1],mskns[a-i]))
        dst.append(cv2.bitwise_or(image[a-i],msked[i]))
        cv2.imshow('dst',dst[i])
        cv2.waitKey(0)

        
    
    #cv2.imshow('msked', msked[0])
    #cv2.waitKey(1)
    #cv2.imshow('dst', dst[a])
    #cv2.waitKey(1)

    #cv2.imwrite('pra.png',dst[a])
    color.append(cv2.cvtColor(dst[-1],cv2.COLOR_GRAY2RGB))
    #cv2.imshow('color', color)
    #cv2.waitKey(1)
    if j % 2 == 1:
        frame_h = cv2.hconcat([color[0],color[1]])
        #print(frame_h.shape)
        out.write(frame_h)
        #cv2.imshow('frame', frame_h)
        #cv2.waitKey(1)
        color.clear()

    #out.write(color[j])

out.release()


'''
print(len(img_array))
for i in range(len(img_array)):
    out.write(img_array[0])
out.release()
'''






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


