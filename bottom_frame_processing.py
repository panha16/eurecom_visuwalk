import cv2
import numpy as np
import math


#idee : calculer la distance des lignes detectees (MAIS seulement celles tout en bas de l'image!!) par rapport à la verticale au centre 

def distance_centre(coord_point):
	#coord_point = [x,y]
	return coord_point[0] - int(width/2)


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
		bottom_frame = frame[int(width/2):width,:]		#cropping the frame to only the bottom part
		very_bottom_frame = frame[int(width/2) + int(width/4):width,:]		#cropping the frame to the very bottom part
		middle_vertical_line =[int(width/2),0,int(width/2),2000]
		bottom_line = [0,int(height/2) - int(height/4),2000,int(height/2) - int(height/4)]


		#converting each video frame to gray
		gray_frame = cv2.cvtColor(very_bottom_frame,cv2.COLOR_BGR2GRAY)
		#using canny edge detection and hough transform to detect edges and lines
		edges = cv2.Canny(gray_frame,50,200)
		#drawing the lines
		lines = cv2.HoughLinesP(edges,20,np.pi/180,200,20)

		try : 
			for line in lines:

				x0,y0,x1,y1 = line[0]				#retrieving lines start and end coordinates

				cv2.line(gray_frame,(x0,y0),(x1,y1),(255,0,0),3)				#drawing the lines on the frame
				cv2.line(gray_frame,(int(width/2),0),(int(width/2),2000),(0,255,0),3)
				cv2.line(gray_frame,(0,int(height/2) - int(height/4)),(2000,int(height/2) - int(height/4)),(0,255,0),3)

				dist_centre = x0 - int(width/2)
				print(dist_centre)

				if dist_centre > 220 : 
					print("LINE ON THE RIGHT")
				if dist_centre < -250 :
					print("LINE ON THE LEFT")

			cv2.imshow('processed frame',gray_frame)

		except :
			print("no lines detected in frame !!!") 

	else : 
		print("no more video input")
		break