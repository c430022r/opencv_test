import cv2
import numpy as np
import glob


imgs = list()
msks = list()
color = list()
count = 0


###    画像の取り出し処理    ####

files = glob.glob("./data/src/*.png")
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
    #cv2.imshow('left',left)
    #cv2.waitKey(0)
    #count+=1
    #print(file)


mskfiles = glob.glob("./data/mask/*.png")
mskfiles = sorted(mskfiles)
for file in mskfiles:
    img = cv2.imread(file)
    width = img.shape[1]
    left = img[:,0:width//2]
    right = img[:,width//2:]
    left = left[35:1044,165:795]
    right = right[35:1044,165:795]
    msks.append(left)
    msks.append(right)
    count+=2
    #print(file)



##   ここに核となる処理を記述する  # #

name = 'tenuri.mp4'   # 動画の名前の宣言
size = (1260,1009)
out = cv2.VideoWriter(name, cv2.VideoWriter_fourcc(*'MP4V'), 30.0, size)

element4 = np.array([[0,1,0],[1,1,1],[0,1,0]],np.uint8) #4近傍
element8 = np.array([[1,1,1],[1,1,1],[1,1,1]],np.uint8) #8近傍

##   回数   ##

su = 20
#roop = su+3


##  段階的ブラー処理  ##

for j in range(0,count,1):
    
    mask = cv2.cvtColor(msks[j],cv2.COLOR_RGB2GRAY)
    #mask = cv2.threshold(mask, 220, 255,cv2.THRESH_BINARY)[1]
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
    

        ##########################################

        if i <= 10:
            blur = cv2.blur(img_blur,(13,13))
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

    
    color.append(cv2.cvtColor(dst,cv2.COLOR_GRAY2RGB))
    #color.append(dst)
    if j % 2 == 1:
        frame_h = cv2.hconcat([color[0],color[1]])
        #print(frame_h.shape)
        out.write(frame_h)
        #cv2.imshow('frame', frame_h)
        #cv2.waitKey(1)
        color.clear()

    #out.write(color[j])


out.release()

