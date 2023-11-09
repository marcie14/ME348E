import cv2
import numpy as np
from random import choice


cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        continue

    # rectangle for user to play
    cv2.rectangle(frame, (25, 25), (300, 300), (255, 255, 255), 2)
    
    # extract the region of image within the user rectangle
    player_move = frame[25:300, 25:300]
    img = cv2.cvtColor(player_move, cv2.COLOR_BGR2GRAY)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = cv2.resize(img, (224, 224))
    img_blur = cv2.GaussianBlur(img, (3,3), 0)
    sobelxy = cv2.Sobel(src=img_blur, ddepth=cv2.CV_64F, dx=1, dy=1, ksize=5)


    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(frame, "Your Move: ", (5, 25), font, 1.2, (5, 180, 30), 2, cv2.LINE_AA)
    k = cv2.waitKey(10)
    if k == ord('q'):
        break
    cv2.imshow("Bird Cow Snake", frame)
cap.release()
cv2.destroyAllWindows()