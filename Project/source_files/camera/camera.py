# turn on camera
import cv2
import numpy as np
from random import choice


cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        continue

    # # rectangle for user to play
    # cv2.rectangle(frame, (25, 25), (300, 300), (255, 255, 255), 2)
    
    # extract the region of image within the user rectangle
    # player_move = frame[25:300, 25:300]
    
    
    # img = cv2.imread('sof.jpg')


    ORANGE_MIN = np.array([0,50,140],np.uint8)
    ORANGE_MAX = np.array([115,170,255],np.uint8)
    # ORANGE_MIN = np.array([5, 50, 50],np.uint8)
    # ORANGE_MAX = np.array([15, 255, 255],np.uint8)

    hsv_img = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)

    frame_threshed = cv2.inRange(hsv_img, ORANGE_MIN, ORANGE_MAX)
    # cv2.imwrite('output2.jpg', frame_threshed)
    
    
    cv2.imshow("Bird Cow Snake", frame_threshed)

    
    # img = cv2.cvtColor(cv2.COLOR_BGR2GRAY)
    # # hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    # img = cv2.resize(img, (224, 224))
    # img_blur = cv2.GaussianBlur(img, (3,3), 0)
    # sobelxy = cv2.Sobel(src=img_blur, ddepth=cv2.CV_64F, dx=1, dy=1, ksize=5)


    # font = cv2.FONT_HERSHEY_SIMPLEX
    # cv2.putText(frame, "Your Move: ", (5, 25), font, 1.2, (5, 180, 30), 2, cv2.LINE_AA)
    k = cv2.waitKey(10)
    if k == ord('q'):
        break
    # mask = cv2.inRange(hsv,(10, 100, 20), (25, 255, 255) )
    # cv2.imshow("Bird Cow Snake", mask)
cap.release()
cv2.destroyAllWindows()
