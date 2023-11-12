#M E 369P - Team 4 - Short n' Clean 
#Allen Hewson, Brenda Miltos, Marcie Legarde, Pranay Srivastava
#Gather Data File:
#    This file captures image data for use in training a model to recognize a hand playing rock paper scissors

# importing required libraries
import cv2
import os

path = r'/Users/marciellelegarde/Desktop/ME348E/'
cwd = os.getcwd() # current working directory

# image_type will be cow, bird, snake, or none 
def get_data(sample_count, image_type):
  capture = cv2.VideoCapture(0)
  start = False
  count = 0
  while True:
    ret, frame = capture.read() 
    cv2.namedWindow('frame', cv2.WINDOW_NORMAL)
    # cv2.setWindowProperty('frame', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    # If nothing is captured just continue
    if not ret:
      continue
    # When you get enough samples stop
    if count == sample_count:
      break
    # Create the frame of what that we will be looking in
    cv2.rectangle(frame, (25, 25), (300, 300), (255, 255, 255), 2)
    # We will have keys to determine if we started taking pictures.
    # Press a to start taking pictures, press q to stop
    key = cv2.waitKey(10)
    if key == ord('a'):
      start = not start
    if key == ord('q'):
      break
    # If we have started collecting data, we will start taking pictures in the defined frame and saving them to the filepath
    if start:
        data_image = frame[25:300, 25:300]
        # Create a path to the drive
        file_path = os.path.join(path, image_type, f"{count}.jpg")
        # file_path = r'\Users\marciellelegarde\Desktop\ME348E\' + image_type + r'\' + str(count) + '.jpg'
        print(file_path)
        cv2.imwrite(file_path , data_image)
        if not cv2.imwrite(file_path , data_image):
          raise Exception("Could not write image")
        count+=1
    # Add an update count for how many images are collected
    cv2.putText(frame, "Collecting {} images".format(count), (5,25), cv2.FONT_HERSHEY_COMPLEX, 0.7, (0, 255, 255), 2, cv2.LINE_AA)
    cv2.imshow("Collecting images", frame)
  capture.release()
  cv2.destroyAllWindows

# get_data(2400, "Cow")
# get_data(2400, "Bird")
# get_data(2400, "Snake")
get_data(100, "Flag")
# get_data(10, "none")