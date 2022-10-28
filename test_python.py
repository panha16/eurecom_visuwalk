import cv2
import numpy as np


video = cv2.VideoCapture("videoligne.mp4")

if not video.isOpened():		#checking if video can and is opened
	print("video can't be opened")

while video.isOpened():
	yes,frame = video.read()		#extracting video frames
	if yes == True :
		frame = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)		#converting frames to gray and using canny edge detection with a high treshold
		edges = cv2.Canny(frame,50,100)
		lines = cv2.HoughLinesP(edges,1,np.pi/180,200)		#last 3 parameters : treshold,minLineLength,maxLineGap
		for line in lines :
			x1,y1,x2,y2 = line[0]
			cv2.line(frame,(x1,y1),(x2,y2),(255,0,0),3)
		#alors ça marche bien mais quand c'est courbe et bah il reconnait rien
		cv2.imshow('hough tranform',frame)
		# contours,hierarchy = cv2.findContours(canny,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
		# print("numbers of objects = %d" % (len(contours)))
		# testdraw = cv2.drawContours(frame, contours, -1, (0,255,0), 5)
		# cv2.imshow('image we draw on',testdraw)

		if cv2.waitKey(25) & 0xFF == ord('q') :				#pressing q will exit the video player
			break

	else :
		break




video.release()
cv2.destroyAllWindows()
