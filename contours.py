import cv2
import time
import numpy as np

videoCapture = cv2.VideoCapture(0)

class Finder:
    x = 0
    y = 0
    w = 0
    h = 0
    color_min = np.array([110, 100, 100], np.uint8)
    color_max = np.array([130, 255, 255], np.uint8)
    
    def __init__(self, color_min, color_max):
        self.color_min = color_min
        self.color_max = color_max
        
    def update(self, frame, hsv_img, a = 0, b = 255, ccCccc = 0):
        frame_threshed = cv2.inRange(hsv_img, self.color_min, self.color_max)
        ret,thresh = cv2.threshold(frame_threshed, 127, 255, 0)
        contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

        areas = [cv2.contourArea(c) for c in contours]
        if areas != []:
            max_index = np.argmax(areas)
            cnt = contours[max_index]

            self.x, self.y, self.w, self.h = cv2.boundingRect(cnt)
            cv2.rectangle(frame, (self.x, self.y), (self.x + self.w, self.y + self.h), (a, b, ccCccc), 2)
            cv2.rectangle(hsv_img, (self.x, self.y), (self.x + self.w, self.y + self.h), (a, b, ccCccc), 2)

        else:
            cv2.rectangle(frame, (self.x, self.y), (self.x + self.w, self.y + self.h), (a, b, ccCccc), 2)
            cv2.rectangle(hsv_img, (self.x, self.y), (self.x + self.w, self.y + self.h), (a, b, ccCccc), 2)

blueMin = np.array([110, 100, 100], np.uint8)
blueMax = np.array([130, 255, 255], np.uint8)
blue = Finder(blueMin, blueMax)

greenMin = np.array([50, 100, 100], np.uint8)
greenMax = np.array([70, 255, 255], np.uint8)
green = Finder(greenMin, greenMax)

while True:
    # Capture frame-by-frame
    ret, frame = videoCapture.read()

    hsv_img = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    blue.update(frame, hsv_img, 255, 0, 0)
    green.update(frame, hsv_img, 0, 255, 0)

    # Display the resulting frame
    #cv2.imshow('frame_threshed', frame_threshed)
    #cv2.imshow('thresh', thresh)
    cv2.imshow('frame', frame)
    cv2.imshow('hsv_img', hsv_img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything is done, release the capture
video_capture.release()
cv2.destroyAllWindows()
