from picamera.array import PiRGBArray
from picamera import picamera
import time
import cv2

camera = PiCamera()
camera.resolution = (640,480)
camera.framerate = 30
rawCapture = PiRGBArray(camera,size = (640,480))


time.sleep(0.1)

for frame in camera.capture_continuous(rawCapture,format = "bgr",use_video_port = True):
	image = frame.array

	#show the frame
	cv2.imshow("Frame",image)
	key = cv2.WaitKey() & 0xFF

	#clear the stream in preparation for the next frame
	rawCapture.truncate()

	if key == ord('q'):
		break