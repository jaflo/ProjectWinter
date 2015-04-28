import cv2
import time
import numpy as np

videoCapture = cv2.VideoCapture(0)

calibrating = True
counter = -1 #how many clicks before calibration ends
color = 0 # color from click
colors = []
totaltime = 0
totaltries = 0
currentstep = "Click the background"

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
		self.previouswidths = []
		self.previousheights = []
		
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
				max_index = np.argmax(areas)
				cnt = contours[max_index]
				nowx, nowy, noww, nowh = cv2.boundingRect(cnt)
				self.previouswidths.append(noww)
				self.previousheights.append(nowh)
				if (threshhold<(float(noww)/float(np.median(self.previouswidths[-30:])))<(1/threshhold)) and (threshhold<(float(nowh)/float(np.median(self.previousheights[-30:])))<(1/threshhold)):
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

#frame = cv2.imread("color_wheel_730.png")

while True:
	ret, frame = videoCapture.read()
	hsv_img = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

	def text(text):
		x = 10
		y = 20
		padding = 3
		global frame
		size = cv2.getTextSize(text, cv2.FONT_HERSHEY_PLAIN, 1, 25)
		cv2.rectangle(frame, (x-padding,y+padding),
			(x+size[0][0]-10*padding,y-size[0][1]/2-padding), 0, -99)
		cv2.putText(frame, text, (10,20), cv2.FONT_HERSHEY_PLAIN, 1, [255,255,255])
	
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
					white = Finder(whiteMin, whiteMax)
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
					blue = Finder(blueMin, blueMax)
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
				green = Finder(greenMin, greenMax)        
				calibrating = False
				colors = []
	else:
		start = time.time()
		# Capture frame-by-frame
		# and show the outlines
		white.update(frame, hsv_img, 0, 0, 0)
		blue.update(frame, hsv_img, 255, 0, 0)
		green.update(frame, hsv_img, 0, 255, 0)
		#print white.color_min
		totaltime+=time.time()-start
		totaltries+=1
		text("FPS: "+str(round(totaltries/totaltime,2)))

	cv2.imshow('frame', frame)
	#cv2.imshow('hsv_img', hsv_img)

	if cv2.waitKey(1) & 0xFF == ord('q'):
		break
	
	time.sleep(1/10.)
# When everything is done, release the capture
video_capture.release()
cv2.destroyAllWindows()
