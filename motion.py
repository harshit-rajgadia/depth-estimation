#! /usr/bin/env python
import argparse
import datetime
import imutils
import time
import cv2

#ap = argparse.ArgumentParser()
#ap.add_argument("-a","--min-area",type = int,default=500,help="minimum area size")
#args= vars(ap.parse_args())
firstFrame = None
cap = cv2.VideoCapture(0)

while True:

	grabbed,frame = cap.read()
	text = "Unoccupied"

	if not grabbed:
		break

	frame = imutils.resize(frame,width=500)
	gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
	gray = cv2.GaussianBlur(gray,(21,21),0)

	if firstFrame is None:
		firstFrame = gray
		continue

	frameDelta  = cv2.absdiff(firstFrame,gray)
	thresh = cv2.threshold(frameDelta,25,255,cv2.THRESH_BINARY)[1]
	thresh = cv2.dilate(thresh,None,iterations= 2)
	(cnts,__) = cv2.findContours(thresh.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

	for c in cnts:
		if cv2.contourArea(c) < 1000:
			continue

		#(x,y,w,h) = cv2.boundingRect(c)
		#cv2.rectangle(frame,(x,y),(x+h,y+w),(0,255,0),2)
		cv2.drawContours(frame,c,-1,(0,255,0),2)
		text = "Occupied"
	cv2.imshow('frameDelta' , frameDelta)
	cv2.imshow('frame' , frame)
	k = cv2.waitKey(1) & 0xFF
	if k == ord('q'):
		break

cap.release()
cv2.destroyAllWindows()
