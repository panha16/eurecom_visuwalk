from picamera.array import PiRGBArray
from picamera import PiCamera
import numpy as np
import time
import cv2
import io
import math


from fifo import *


class NoLineBottom(Exception):
    pass

def get_barycentre(image, start_y, end_y):
    ''' Computes the barycentre of white points
    in a given y range for a BW image '''
    y_avg = 0
    x_avg = 0
    n = 0

    for y in range(start_y, end_y):
        for x in range(0, len(image[0])):
            if(image[y,x] == 255):
                y_avg += y
                x_avg += x
                n += 1

    if(n != 0):
        y_avg /= n
        x_avg /= n

        return (int(y_avg), int(x_avg))
    else:
        raise NoLineBottom


def get_angle_vertical(y,x):
    ''' Computes the oriented angle of a vector
    with the y axis (vertical line on the image)'''
    mag = math.sqrt(x**2 + y**2)
    cos_val = y/mag
    angle_val = math.acos(cos_val)
    direction = x/abs(x) if x != 0 else 1
    angle_val = direction*angle_val
    angle_val = angle_val*180/np.pi
    return angle_val


def get_distance_middle(image, start_y, end_y):
    ''' Computes the distance between the middle
    of the image and the line on a given y range'''
    y,point = get_barycentre(image, start_y, end_y)
    width = len(image[0])
    return abs(point-width/2)


height=320
width=240
camera = PiCamera()
camera.resolution = (height,width)
camera.framerate = 30
rawCapture = PiRGBArray(camera,size = (height,width))

avg_gamma = create_queue(4)

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

    # detecting the lines for the half-bottom part of the image
    lines = cv2.HoughLinesP(edges[int(height/2):,:],rho=20,theta=np.pi/45,threshold=30,minLineLength=4)
    # look through whole image if no line is detected
    if(type(lines) is not np.ndarray):
        lines = cv2.HoughLinesP(edges,rho=20,theta=np.pi/45,threshold=30,minLineLength=4)

    alpha = 0 # alpha angle (cf. documentation)

    if(type(lines) is np.ndarray):
        for line in lines:

            # x axis is horizontal right-leaning, y axis is vertical descendant
            x0,y0,x1,y1 = line[0]				#retrieving lines start and end coordinates
            if y0>y1:
                y0,y1 = y1,y0                   # rearrange lines for orientation calculation
                x0,x1 = x1,x0

            y = y1-y0
            x = x1-x0
            alpha += get_angle_vertical(y,x)

        alpha /= len(lines)
        alpha = alpha if abs(alpha) <= 70 else 70*(alpha/abs(alpha))

        try:
            d = get_distance_middle(edges, int(4*height/5), height)
        except NoLineBottom:
            d = get_distance_middle(edges, 0, height)   # look through whole image if no line detected in wanted bounds

        try:
            tp_y, tp_x = get_barycentre(edges, int(height/2), int(2*height/3))  # target point coordinates
        except NoLineBottom:
            tp_y, tp_x = get_barycentre(edges, 0, height)   # look through whole image if no line detected in wanted bounds
        cv2.line(edges,(tp_x,tp_y),(tp_x,tp_y),(255,0,0),3)

        # transform coordinates into vector with tp as start point and bottom of middle vertical line
        # as end point
        tp_y = height - tp_y
        tp_x = int(width/2) - tp_x
        beta = get_angle_vertical(tp_y, tp_x)

        gamma = alpha + (1 - math.exp(-6*d/width))*(beta-alpha)
        print("gamma = ", gamma)

        add_element(gamma, avg_gamma)
        print("avg gamma = ", avg_queue(avg_gamma))

    else:
        print("no lines detected in frame !!!") 
        gamma = 100     # value out of the bounds, to notify that no angle was detected

    # clear the stream in preparation for the next frame
    rawCapture.truncate(0)
