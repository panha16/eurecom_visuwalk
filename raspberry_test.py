import time
import picamera
import io 
from imutils.video import VideoStream
import datetime
import argparse
import imutils
import time
import cv2

# with picamera.PiCamera() as camera :
# 	smtrea = io.BytesIO()
# 	for foo in camera.capture_continuous(stream,format ="jpeg"):
# 		stream.truncate()
# 		

from webcamvideostream import webcamvideostream
class VideoStream:
	def __init__(self,src = 0,resolution = (1640,1232),framerate = 30):
		from pivideostream import PiVideoStream
		self.stream = PiVideoStream(resolution = resolution, framerate = framerate)

	def start(self):
		#start the video stream
		return self.stream.start()

	def update(self):
		#grab the next frame from the stream
		self.stream.update()

	def read(self):
		#return the current frame
		return self.stream.read()

	def stop(self):
		self.stream.stop()
		

vs = VideoStream(usePicamera = True).start()
time.sleep(2.0)

while True :
	frame = vs.read()

	# draw the timestamp on the frame
	timestamp = datetime.datetime.now()
	ts = timestamp.strftime("%A %d %B %Y %I:%M:%S%p")
	cv2.putText(frame, ts, (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX,
		0.35, (0, 0, 255), 1)

	cv2.imshow("video !!",frame)

cv2.DestroyAllWindows()
vs.stop()

