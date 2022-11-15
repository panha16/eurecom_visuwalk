import cv2
import numpy as np
import math
import pygame

#sound init
pygame.init()
pygame.display.set_caption("audio test")

hz300 = pygame.mixer.Sound("300Hz.MP3")
hz1200 = pygame.mixer.Sound("1200Hz.MP3")
hz300.play()
hz1200.play()
hz1200.set_volume(0)
hz300.set_volume(0)

#vector should like the following way : [x0,y0,x1,y1]

#defining scalar product function
def dot(vector_a,vector_b):
	return vector_a[0]*vector_b[0] + vector_a[1]*vector_b[1]

#defining a function to calculate the angle between two vectors using a.b = |a||b|cos angle

def line_angle(vecA,vecB):
	vA = [(vecA[0] - vecA[2]),(vecA[1] - vecA[3])]
	vB = [(vecB[0] - vecB[2]),(vecB[1] - vecB[3])]
	dot_product = dot(vA,vB)
	magA = dot(vA,vA) ** 0.5 #magA = |a|
	magB = dot(vB,vB) ** 0.5 #magB = |b|
	angle_cosine = dot_product/magA/magB
	angle = math.acos(angle_cosine)
	return angle

#opening the video file
video = cv2.VideoCapture("videoligne.mp4")


#checking if video can be opened
if not video.isOpened():
	print("video can't be opened")


while video.isOpened():

	#retrieving video frame and dimensions
	video_bool,frame = video.read()

	if video_bool :

		if cv2.waitKey(25) == ord('q') :				#pressing q will exit the video player
			break
		if cv2.waitKey(40) == ord('p') :				#pressing p will pause the video
			cv2.waitKey(0)	


		frame = frame[0:1640,0:1232]		#cropping the frame to match the camera module video dimensions

		height,width = frame.shape[0],frame.shape[1]
		upper_frame = frame[0:int(width/2),:]		#cropping the frame to only the upper-part

		middle_vertical_line =[int(width/2),0,int(width/2),2000]

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
						hz300.set_volume(1),hz1200.set_volume(0)
					else :
						print ("LEFT")
						hz300.set_volume(0.5),hz1200.set_volume(0)
				if angle_value > 1 :
					if angle_value > 3 :
						print("SHARP RIGHT")
						hz1200.set_volume(1),hz300.set_volume(0)
					else :
						print ("RIGHT")
						hz1200.set_volume(0.5),hz300.set_volume(0)
			cv2.imshow('processed frame',gray_frame)
		except :
			print("no lines detected in frame !!!") 

	else : 
		print("no more video input")
		break
