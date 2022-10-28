import cv2



video = cv2.VideoCapture("videoligne.mp4")

if not video.isOpened():
	print("video can't be opened")

while video.isOpened():
	yes,frame = video.read()
	if yes == True :
		frame = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
		canny = cv2.Canny(frame,50,150)
		cv2.imshow('Frame',canny)

		if cv2.waitKey(25) & 0xFF == ord('q') :
			break

	else :
		break

video.release()
cv2.destroyAllWindows()
