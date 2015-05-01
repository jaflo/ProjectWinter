"""
Lots of code by glooga, although he did not commit
"""

import cv2
from PIL import Image
import serial
import time
import numpy as np

videoCapture = cv2.VideoCapture(0)

calibrating = True
counter = -1 #how many clicks before calibration ends
color = 0 # color from click
colors = []
trytime = [] #will contain the time to process a frame
currentstep = "Click the background"

class Finder:
        x = 0
        y = 0
        w = 0
        h = 0
        comPort = "COM5"
        color_min = np.array([110, 100, 100], np.uint8)
        color_max = np.array([130, 255, 255], np.uint8)
        ser = None
        
        def __init__(self, color_min, color_max, comPort = "COM3", sender = False):
                self.color_min = color_min
                self.color_max = color_max
                self.previouswidths = []
                self.previousheights = []
                self.comPort = comPort
                if sender:
                        self.ser = serial.Serial(self.comPort, 19200)

        def send(self, whiteblock):
                heh = ""
                wx = whiteblock.x
                wy = whiteblock.y
                px = int((wx - self.x)/40) + 1
                if px > 32:
                        px = 32
                if px < 0:
                        px = 0
                py = int((wy - self.y)/40) + 1
                if py > 32:
                        py = 32
                if py < 0:
                        py = 0

                try:
                        print "sending"
                        im = Image.open("demo/frame.png") # take an image
                        im = im.crop((px, py, px + 8, py + 8))
                        im.save("part.png")
                        sers = self.ser
                        rgb_im = im.convert("RGB") # convert to RGB color space
                        for x in range(0, 8):
                            for y in range(0, 8):
                                # for each pixel, get rgb, convert to hex
                                heh += "%02x%02x%02x"%rgb_im.getpixel((x, y))
                        heh += "q" # terminating 'q'
                        for c in heh: # write data byte by byte
                            sers.write(c)
                            #print ser.read(ser.inWaiting()) # DEBUG
                except:
                        print "failed, retrying..." # shown when any error occurs
                
        def update(self, frame, hsv_img, a = 0, b = 255, ccCccc = 0):
                frame_threshed = cv2.inRange(hsv_img, self.color_min, self.color_max)
                ret,thresh = cv2.threshold(frame_threshed, 127, 255, 0)
                contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

                def recupdate(contours):
                        areas = [cv2.contourArea(c) for c in contours]
                        
                        def showprev():
                                cv2.rectangle(frame, (self.x, self.y), (self.x + self.w, self.y + self.h), (a, b, ccCccc), 2)
                                cv2.rectangle(hsv_img, (self.x, self.y), (self.x + self.w, self.y + self.h), (a, b, ccCccc), 2)

                        if areas != []:
                                threshhold = 0.9
                                oflast = 30 #frames
                                max_index = np.argmax(areas)
                                cnt = contours[max_index]
                                nowx, nowy, noww, nowh = cv2.boundingRect(cnt)
                                self.previouswidths.append(noww)
                                self.previousheights.append(nowh)
                                if (threshhold<(float(noww)/float(np.median(self.previouswidths[-oflast:])))<(1/threshhold)) and (threshhold<(float(nowh)/float(np.median(self.previousheights[-oflast:])))<(1/threshhold)):
                                        Height, Width, trash = frame.shape
                                        self.x, self.y, self.w, self.h = cv2.boundingRect(cnt)
                                        if (0.95 < self.w/self.h < 1/0.95) or len(contours) == 1:
                                                cv2.rectangle(frame, (self.x, self.y), (self.x + self.w, self.y + self.h), (a, b, ccCccc), 2)
                                                cv2.rectangle(hsv_img, (self.x, self.y), (self.x + self.w, self.y + self.h), (a, b, ccCccc), 2)
                                        else:
                                                contours = contours[:max_index] + contours[max_index + 1:]
                                                recupdate(contours)
                                else:
                                        showprev()
                        else:
                                showprev()
                recupdate(contours)

def clicker(event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
                global color
                global colors
                color = hsv_img[y][x]
                colors = colors + [color]
                global counter
                counter += 1

def text(text):
        x = 10
        y = 20
        padding = 1
        global frame
        size = cv2.getTextSize(text, cv2.FONT_HERSHEY_PLAIN, 1, 25)
        cv2.rectangle(frame, (x-padding,y+padding),
                (x+size[0][0]-15,y-size[0][1]/2-padding), 0, -99)
        cv2.putText(frame, text, (10,20), cv2.FONT_HERSHEY_PLAIN, 1, [255,255,255])


while True:
        start = time.time()
        ret, frame = videoCapture.read()
        hsv_img = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        if calibrating:
                text(currentstep)
                cv2.setMouseCallback("frame", clicker)
                if counter/4 == 0:
                        if counter%4 == 3:
                                if colors != []:
                                        currentstep = "Click the blue frame"
                                        h = [a[0] for a in colors]
                                        h.sort()
                                        s = [a[1] for a in colors]
                                        s.sort()
                                        v = [a[2] for a in colors]
                                        v.sort()
                                        whiteMin = np.array([h[0]-10, s[0]-10, v[0]-10], np.uint8)
                                        whiteMax = np.array([h[3]+10, s[3]+10, v[3]+10], np.uint8)
                                        white = Finder(whiteMin, whiteMax, comPort = "COM3")
                                colors = []
                elif counter/4 == 1:
                        if counter%4 == 3:
                                if colors != []:
                                        currentstep = "Click the green frame"
                                        h = [a[0] for a in colors]
                                        h.sort()
                                        s = [a[1] for a in colors]
                                        s.sort()
                                        v = [a[2] for a in colors]
                                        v.sort()
                                        blueMin = np.array([h[0]-10, s[0]-10, v[0]-10], np.uint8)
                                        blueMax = np.array([h[3]+10, s[3]+10, v[3]+10], np.uint8)
                                        blue = Finder(blueMin, blueMax, comPort = "COM3", sender = True)
                                colors = []
                elif counter/4 == 2:
                        if counter%4 == 3:
                                h = [a[0] for a in colors]
                                h.sort()
                                s = [a[1] for a in colors]
                                s.sort()
                                v = [a[2] for a in colors]
                                v.sort()
                                greenMin = np.array([h[0]-10, s[0]-10, v[0]-10], np.uint8)
                                greenMax = np.array([h[3]+10, s[3]+10, v[3]+10], np.uint8)
                                green = Finder(greenMin, greenMax, comPort = "COM3")        
                                calibrating = False
                                colors = []
        else:
                # Capture frame-by-frame
                # and show the outlines
                white.update(frame, hsv_img, 0, 0, 0)
                blue.update(frame, hsv_img, 255, 0, 0)
                green.update(frame, hsv_img, 0, 255, 0)
                blue.send(white)
                #print white.color_min
                trytime.append(time.time()-start)
                text("FPS: "+str(round(1/np.mean(trytime[-20:]),2)))
        
        cv2.imshow('frame', frame)
        #cv2.imshow('hsv_img', hsv_img)

        if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        time.sleep(1/10.)

video_capture.release()
cv2.destroyAllWindows()
