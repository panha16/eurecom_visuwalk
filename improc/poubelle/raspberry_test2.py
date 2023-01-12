from picamera.array import PiRGBArray
from picamera import PiCamera
import numpy as np
import time
import cv2
import io

camera = PiCamera()
camera.resolution = (640,480)
width=480
height=640
camera.framerate = 30
rawCapture = PiRGBArray(camera,size = (640,480))


time.sleep(0.1)

for frame in camera.capture_continuous(rawCapture,format = "bgr",use_video_port = True):
	frame = frame.array
	upper_frame = frame[0:int(width/2),:]		#cropping the frame to only the upper-part
	middle_vertical_line =[int(width/2),0,int(width/2),height]

	#converting each video frame to gray
	gray_frame = cv2.cvtColor(upper_frame,cv2.COLOR_BGR2GRAY)
	#using canny edge detection and hough transform to detect edges and lines
	edges = cv2.Canny(gray_frame,50,200)
	#drawing the lines
	lines = cv2.HoughLinesP(edges,20,np.pi/180,200,20)
	
	try : 
		for line in lines:

			x0,y0,x1,y1 = line[0]				#retrieving lines start and end coordinates

			cv2.line(gray_frame,(x0,y0),(x1,y1),(255,0,0),3)				#drawing the lines on the frame

			#calculating the angle between the detected lines and the middle vertical line
			angle_value = line_angle(middle_vertical_line,line[0])
		
			if angle_value < 1 :
				if angle_value > 0.6 :
					print("SHARP LEFT")
				else :
					print ("LEFT")
			if angle_value > 1 :
				if angle_value > 3 :
					print("SHARP RIGHT")
				else :
					print ("RIGHT")

		cv2.imshow('processed frame',gray_frame)
		#clear the stream in preparation for the next frame
		rawCapture.truncate(0)

	except :
		print("no lines detected in frame !!!") 
		rawCapture.truncate(0)


