import numpy as np
import cv2
import os
import datetime
import sys


file_src_path = ''
file_src_name = '20200218_102324_0_0'
file_src_ext = '.avi'
file_src = file_src_path + file_src_name + file_src_ext
file_dst = file_src_name

drawing_L = False
drawing_R = False

pen_size = 20
pen_pos = (0, 0)

frame_skip = 10 - 1

flag_mask = True

def draw_circle(event, x, y, flags, param):
    global drawing_L, drawing_R, pen_size, pen_pos
    pen_pos = (x, y)
    
    if event == cv2.EVENT_MOUSEWHEEL:
        if flags > 0:
            pen_size += 1
        else:
            pen_size -= 1
            pen_size = max(1, pen_size)
    
    if event == cv2.EVENT_LBUTTONDOWN:
        drawing_L = True
    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing_L == True:
            cv2.circle(img_mask, (x, y), pen_size, (255, 255, 255), -1)
    elif event == cv2.EVENT_LBUTTONUP:
        drawing_L = False
        cv2.circle(img_mask, (x, y), pen_size, (255, 255, 255), -1)

    if event == cv2.EVENT_RBUTTONDOWN:
        drawing_R = True
    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing_R == True:
            cv2.circle(img_mask, (x, y), pen_size, (0, 0, 0), -1)
    elif event == cv2.EVENT_RBUTTONUP:
        drawing_R = False
        cv2.circle(img_mask, (x, y), pen_size, (0, 0, 0), -1)


def terminate():
    cap.release()
    cv2.destroyAllWindows()
    sys.exit()

##########################################################
cap = cv2.VideoCapture(file_src)
if not cap.isOpened():
    print('=== cap error ===')
    terminate()

frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

try:
    input_num = int(input("input start frame number.: "))
except ValueError:
    print("retry it again!")
    terminate()

cap.set(cv2.CAP_PROP_POS_FRAMES, input_num -1)

cv2.namedWindow('src')
cv2.setMouseCallback('src', draw_circle)

folder = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
os.makedirs(folder)

while(True):
    ret, img_src = cap.read()
    img_mask = np.zeros((img_src.shape[0], img_src.shape[1], img_src.shape[2]), np.uint8)
    img_mouse = np.zeros((img_src.shape[0], img_src.shape[1], img_src.shape[2]), np.uint8)

    frame_pos = int(cap.get(cv2.CAP_PROP_POS_FRAMES))
    print(str(frame_pos) + ' / ' + str(frame_count))
    
    while(True):
        img_disp = cv2.bitwise_and(img_src, cv2.bitwise_not(img_mask), img_mouse)
        img_masked = cv2.bitwise_and(img_src, cv2.bitwise_not(img_mask))
        
        cv2.circle(img_mouse, pen_pos, pen_size, (255, 255, 255), 1)
        if flag_mask:
            cv2.imshow('src', img_disp)
        else:
             cv2.imshow('src', img_src)
        ch = cv2.waitKey(10)
        img_mouse.fill(0)
        
        if ch == ord('r'):
            img_mask.fill(0)
        elif ch == ord(' '):
            flag_mask =  not flag_mask
        elif ch == ord('n') or ch == ord('q'):
            flag_mask = True
            break
        elif ch == ord('s'):
            cv2.imwrite(folder + '/' + file_dst + '_' + str(frame_pos).zfill(4) + '_' + str(frame_count).zfill(4)+ '_mask.png', img_mask)
            cv2.imwrite(folder + '/' + file_dst + '_' + str(frame_pos).zfill(4) + '_' + str(frame_count).zfill(4)+ '_masked.png', img_masked)
            cv2.imwrite(folder + '/' + file_dst + '_' + str(frame_pos).zfill(4) + '_' + str(frame_count).zfill(4)+ '_src.png', img_src)
    
    cv2.rectangle(img_mask, (0, 0), (img_mask.shape[1], 34), (255, 255, 255), -1)
    cv2.rectangle(img_mask, (0, 0), (164, img_mask.shape[0]), (255, 255, 255), -1)
    cv2.rectangle(img_mask, (795, 0), (1124, img_mask.shape[1]), (255, 255, 255), -1)
    cv2.rectangle(img_mask, (1755, 0), (img_mask.shape[1], img_mask.shape[0]), (255, 255, 255), -1)
    cv2.rectangle(img_mask, (0, 1044), (img_mask.shape[1], img_mask.shape[0]), (255, 255, 255), -1)
    
    cv2.imwrite(folder + '/' + file_dst + '_' + str(frame_pos).zfill(4) + '_' + str(frame_count).zfill(4)+ '_mask.png', img_mask)
    cv2.imwrite(folder + '/' + file_dst + '_' + str(frame_pos).zfill(4) + '_' + str(frame_count).zfill(4)+ '_masked.png', img_masked)
    cv2.imwrite(folder + '/' + file_dst + '_' + str(frame_pos).zfill(4) + '_' + str(frame_count).zfill(4)+ '_src.png', img_src)

    if ch == ord('q'):
       break
    elif ch == ord('n'):
        if (frame_pos + frame_skip) >= frame_count:
            break
        else:
            cap.set(cv2.CAP_PROP_POS_FRAMES, frame_pos + frame_skip)

terminate()



