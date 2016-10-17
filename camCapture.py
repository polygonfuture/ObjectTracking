# Standard imports
import cv2
import numpy as np;

cap = cv2.VideoCapture(0)

#Define codec and create VideoWriter object
capSize = (1028,720)
fps = 24
fourcc = cv2.VideoWriter_fourcc('m','p','4','v')
out = cv2.VideoWriter('output.mov',fourcc,fps,capSize)

while (cap.isOpened()):
	#capture frame-by-frame
	ret, frame = cap.read()
	if ret == True:

		#flip image (mirrored by default)
		#frame = cv2.flip(frame,0)

		#grayscale image
		frame = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)

		#write flipped image
		out.write(frame)

		#display resulting frame
		cv2.imshow('frame',frame)

		if cv2.waitKey(24) == 27:
			break
			cap.release()
			cv2.destroyAllWindows()

		#when everything is done release capture