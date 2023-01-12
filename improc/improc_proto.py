import numpy as np
import time
import cv2
import io
import math



#vector should like the following way : [x0,y0,x1,y1]

#defining scalar product function
def dot(vector_a,vector_b):
	return vector_a[0]*vector_b[0] + vector_a[1]*vector_b[1]

#defining a function to calculate the angle between two vectors using a.b = |a||b|cos angle

def line_angle(vecA,vecB):
    vA = [(vecA[2] - vecA[0]),(vecA[3] - vecA[1])]
    vB = [(vecB[2] - vecB[0]),(vecB[3] - vecB[1])]
    dot_product = dot(vA,vB)
    magA = dot(vA,vA) ** 0.5 #magA = |a|
    magB = dot(vB,vB) ** 0.5 #magB = |b|
    angle_cosine = dot_product/(magA*magB)

    '''determinant = (vA[0]*vB[1] - vA[1]*vB[0])
    direction = determinant/abs(determinant) if determinant != 0 else 1
    print(direction)'''
    direction = vB[1]/abs(vB[1])
    
    angle = direction*math.acos(angle_cosine)
    angle = angle*180/math.pi
    return angle



#converting each video frame to gray
# in imread, the first variable (x) is the descendant vertical axis
# the second variable is the right-leaning horizontal axis
# the rest is inverted
gray_frame = cv2.imread("samples/reel3.jpg",cv2.IMREAD_GRAYSCALE)

# applying bilateral filter because of the pattern of the carpet:
# blurring noise while keeping edges sharp
#cv2.imshow('before',gray_frame)
gray_frame = cv2.bilateralFilter(gray_frame, 9, 75, 75)
#cv2.imshow('after', gray_frame)

height,width = gray_frame.shape[0],gray_frame.shape[1]

middle_vertical_line =[int(width/2), 0, int(width/2), height]

#using canny edge detection and hough transform to detect edges and lines
edges = cv2.Canny(gray_frame,50,200)
cv2.imshow('edges', edges)

#drawing the lines
lines = cv2.HoughLinesP(edges,rho=20,theta=np.pi/45,threshold=30,minLineLength=4)

cv2.line(gray_frame,(int(width/2),0), (int(width/2), height),(255,0,0),5)
try : 
    for line in lines:

        x0,y0,x1,y1 = line[0]				#retrieving lines start and end coordinates
        '''if y0>y1:
            y0,y1 = y1,y0                   # rearrange lines for orientation calculation
            x0,x1 = x1,x0'''

        if y0<y1:
            cv2.line(gray_frame,(x0,y0),(x1,y1),(0,0,0),3)				#drawing the lines on the frame
        else:
            cv2.line(gray_frame,(x0,y0),(x1,y1),(255,0,0),3)				#drawing the lines on the frame


        #calculating the angle between the detected lines and the middle vertical line
        angle_value = line_angle(middle_vertical_line,line[0])

        print(angle_value)
    

except :
    print("no lines detected in frame !!!") 

cv2.imshow('processed frame',gray_frame)
k = cv2.waitKey(0)
exit()
