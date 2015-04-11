from PIL import Image
import serial
import time
ser = serial.Serial("COM3", 19200) # make sure this is the right channel
print "flushing..."
heh = "qq" # clear the screen
ser.write(heh) # push the 
print "initialized!"
totaltime = 0
totaltries = 0

while True:
    #print "generating..."
    try:
        start = time.time()
        im = Image.open("demo/frame.png") # take an image
        rgb_im = im.convert("RGB") # convert to RGB color space
        for x in range(0, 8):
            for y in range(0, 8):
                    # for each pixel, get rgb, convert to hex
                heh += "%02x%02x%02x"%rgb_im.getpixel((x, y))
        heh += "q" # terminating 'q'
        #print "transfer:", heh
        for c in heh: # write data byte by byte
            ser.write(c)
            #print ser.read(ser.inWaiting()) # DEBUG
        totaltime+=time.time()-start
        totaltries+=1
        print "done, FPS:",round(totaltries/totaltime,2)
        heh = "" # empty the payload
    except:
        print "failed, retrying..." # shown when any error occurs
