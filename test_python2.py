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
		lines = cv2.HoughLinesP(edges,20,np.pi/180,200)		#last 3 parameters : treshold,minLineLength,maxLineGap
		for line in lines :
			x1,y1,x2,y2 = line[0]
			slope = y1-y2/x1-x2
			length_line = [x2-x1,y2-y1]
			if length_line[0] > 10 or length_line[1] > 10 :		#we only process long lines
				cv2.line(frame,(x1,y1),(x2,y2),(255,0,0),3)
				print(line[0])
				if slope > 0 :
					print("turn left")
				if slope < 0 :
					print("turn right")				#doesnt work !!! 90%, it says to go left wtf	
		cv2.imshow('hough tranform',frame)

		if cv2.waitKey(25) == ord('q') :				#pressing q will exit the video player
			break
		if cv2.waitKey(40) == ord('p') :				#pressing p will pause the video
			cv2.waitKey(0)	

	else :
		break




video.release()
cv2.destroyAllWindows()
