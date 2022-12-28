import cv2
import numpy as np


video = cv2.VideoCapture("videoligne.mp4")

if not video.isOpened():		#checking if video can and is opened
	print("video can't be opened")

while video.isOpened():
	yes,frame = video.read()		#extracting video frames
	height = frame.shape[0]
	width = frame.shape[1]
	if yes == True :
		frame = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)		#converting frames to gray and using canny edge detection with a high treshold
		edges = cv2.Canny(frame,50,200)
		# left_side =edges[0:int(width/2),0:int(height/2)]
		# right_side = edges[int(width/2):width,int(height/2):int(height)]
		# cnt1,hierarchy1 = cv2.findContours(left_side,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)		#counting the numbers of contours 
		# cnt2,hierarchy2 = cv2.findContours(right_side,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)		#counting the numbers of contours 


		lines = cv2.HoughLinesP(edges,20,np.pi/180,200)		#last 3 parameters : treshold,minLineLength,maxLineGap
		left_side = edges[0:int(height/2),0:int(width/2)]
		right_side = edges[int(height/2):height,int(width/2):width]			
		count_left, __ = cv2.findContours(left_side,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
		count_right,__ = cv2.findContours(right_side,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
		elmts_right = len(count_right)
		elmts_left = len(count_left)
		for line in lines :
			x1,y1,x2,y2 = line[0]
			cv2.line(frame,(x1,y1),(x2,y2),(255,0,0),3)
			# cv2.line(frame,(round(width/2),0),(round(width/2),2000),(0,255,0),5)		#drawing the middle line
			if elmts_right > elmts_left :
				print("turn right")
			elif elmts_right < elmts_left :
				print("turn left")
			else : 
				print("keep going straight")
			
		cv2.imshow('hough tranform',frame)

		if cv2.waitKey(25) == ord('q') :				#pressing q will exit the video player
			break
		if cv2.waitKey(40) == ord('p') :				#pressing p will pause the video
			cv2.waitKey(0)	

	else :
		break




video.release()
cv2.destroyAllWindows()
