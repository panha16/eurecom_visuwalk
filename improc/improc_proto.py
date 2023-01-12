import numpy as np
import time
import cv2
import math



# converting each video frame to gray
# in imread, the first variable (y) is the descendant vertical axis
# the second variable (x) is the right-leaning horizontal axis
gray_frame = cv2.imread("samples/reel3.jpg",cv2.IMREAD_GRAYSCALE)

# applying bilateral filter because of the pattern of the carpet:
# blurring noise while keeping edges sharp
# cv2.imshow('before',gray_frame)
gray_frame = cv2.bilateralFilter(gray_frame, 9, 75, 75)
# cv2.imshow('after', gray_frame)

height,width = gray_frame.shape[0],gray_frame.shape[1]

# gray_frame = gray_frame[int(height/2):,int(width/2):]
# gray_frame = gray_frame[:int(height/2),:]

middle_vertical_line =[int(width/2), 0, int(width/2), height]

# using canny edge detection and hough transform to detect edges and lines
edges = cv2.Canny(gray_frame,50,200)
cv2.imshow('edges', edges)

# detecting the lines
lines = cv2.HoughLinesP(edges,rho=20,theta=np.pi/45,threshold=30,minLineLength=4)

cv2.line(gray_frame,(int(width/2),0), (int(width/2), height),(255,0,0),5)


if(type(lines) is np.ndarray):
    for line in lines:

        # x axis is horizontal right-leaning, y axis is vertical descendant
        x0,y0,x1,y1 = line[0]				#retrieving lines start and end coordinates
        if y0>y1:
            y0,y1 = y1,y0                   # rearrange lines for orientation calculation
            x0,x1 = x1,x0                   # -> orienting vector downward

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

else:
    print("no lines detected in frame !!!") 

cv2.imshow('processed frame',gray_frame)
k = cv2.waitKey(0)
exit()
