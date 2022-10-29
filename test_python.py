import cv2
import numpy as np


video = cv2.VideoCapture("videoligne.mp4")

if not video.isOpened():		#checking if video can and is opened
	print("video can't be opened")

while video.isOpened():
	yes,frame = video.read()		#extracting video frames
	if yes == True :
		frame = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)		#converting frames to gray and using canny edge detection with a high treshold
		edges = cv2.Canny(frame,50,200)
		lines = cv2.HoughLinesP(edges,20,np.pi/180,200)		#last 3 parameters : treshold,minLineLength,maxLineGap
		for line in lines :
			x1,y1,x2,y2 = line[0]
			cv2.line(frame,(x1,y1),(x2,y2),(255,0,0),3)
		#alors ça marche bien mais quand c'est courbe et bah il reconnait rien
		cv2.imshow('hough tranform',frame)

		if cv2.waitKey(25) == ord('q') :				#pressing q will exit the video player
			break
		if cv2.waitKey(40) == ord('p') :				#pressing p will pause the video
			cv2.waitKey(0)	

	else :
		break




video.release()
cv2.destroyAllWindows()
