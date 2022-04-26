# import OpenCV library
import cv2
# import Numerical Python library
import numpy as np

# read the colured photo from file
cap = cv2.VideoCapture('1.mp4')

while(cap.isOpened()):
    ret, frame = cap.read()
    if ret == True:
        # gray_img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blur_img = cv2.GaussianBlur(frame, (15, 15), 0)
        edge_img = cv2.Canny(blur_img, 50, 150)
        dilation_kernel = np.ones((4, 4), np.uint8)
        dilated_img = cv2.dilate(edge_img, dilation_kernel, iterations=1)
        cv2.imshow('Blurred',blur_img)
        cv2.imshow('Original', frame)
        cv2.imshow('Canny Edge', edge_img)
        cv2.imshow('Dilated Video', dilated_img)
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break
    else:
        break
# display original colured photo
cap.release()

# block key press
# cv2.waitKey(0)
# destroy previous windows and finish process
cv2.destroyAllWindows()


