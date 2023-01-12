from picamera.array import PiRGBArray
from picamera import PiCamera
import numpy as np
import time
import cv2
import io
import math

camera = PiCamera()
camera.resolution = (640,480)
width=480
height=640
camera.framerate = 30
rawCapture = PiRGBArray(camera,size = (640,480))


for frame in camera.capture_continuous(rawCapture,format = "bgr",use_video_port = True):
    frame = frame.array

    #converting each video frame to gray
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # applying bilateral filter because of the pattern of the carpet:
    # blurring noise while keeping edges sharp
    gray_frame = cv2.bilateralFilter(gray_frame, 9, 75, 75)

    height,width = gray_frame.shape[0],gray_frame.shape[1]

    # using canny edge detection and hough transform to detect edges and lines
    edges = cv2.Canny(gray_frame,50,200)

    # detecting the lines
    lines = cv2.HoughLinesP(edges,rho=20,theta=np.pi/45,threshold=30,minLineLength=4)

    if(type(lines) is np.ndarray):
        for line in lines:

            # x axis is horizontal right-leaning, y axis is vertical descendant
            x0,y0,x1,y1 = line[0]				#retrieving lines start and end coordinates
            if y0>y1:
                y0,y1 = y1,y0                   # rearrange lines for orientation calculation
                x0,x1 = x1,x0

            if y0<y1:
                cv2.line(gray_frame,(x0,y0),(x1,y1),(0,0,0),3)				#drawing the lines on the frame
            else:
                cv2.line(gray_frame,(x0,y0),(x1,y1),(255,0,0),3)				#drawing the lines on the frame


            #calculating the angle between the detected lines and the middle vertical line
            y = y1-y0
            x = x1-x0
            mag = math.sqrt(x**2 + y**2)
            cos_val = y/mag             # it is the cosine if we consider the y descendant axis as the reference
            angle_val = math.acos(cos_val)
            direction = x/abs(x) if x != 0 else 1
            angle_val = direction*angle_val
            angle_val = angle_val*180/np.pi

            print(angle_val)

            # clear the stream in preparation for the next frame
            rawCapture.truncate(0) 

    else:
        print("no lines detected in frame !!!") 
        
        # clear the stream in preparation for the next frame
        rawCapture.truncate(0) 


