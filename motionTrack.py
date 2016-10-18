# import the necessary packages
import argparse
import datetime
import imutils
import time
import cv2
import numpy as np

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", help="path to the video file")
ap.add_argument("-a", "--min-area", type=int, default=500, help="minimum area size")
args = vars(ap.parse_args())

# if the video argument is None, then we are reading from webcam
if args.get("video", None) is None:
	camera = cv2.VideoCapture(0)
	time.sleep(0.25)

# otherwise, we are reading from a video file
else:
	camera = cv2.VideoCapture(args["video"])

# initialize the first frame in the video stream
firstFrame = None

#############################
# CONTROLS #
###########################

title = "Threshold Controls"
cv2.namedWindow(title)
# create emtpy NumPy array to resizse trackbars
emptyControl = np.zeros((50,350), dtype = "uint8")

def on_minThreshold(z):
    threshLO = cv2.getTrackbarPos('Min Threshold',title)
    print ('Low Threshold:' + threshLO)

def on_maxThreshold(z):
    threshHI = cv2.getTrackbarPos('Max Threshold',title)
    print ('Hi Threshold:' + threshHI)

def on_dilateThreshold(z):
    threshHI = cv2.getTrackbarPos('Max Threshold',title)
    print ('Dilate Threshold:' + threshDI)

def threshSTART():
    threshLO = cv2.getTrackbarPos('Min Threshold',title)
    threshHI = cv2.getTrackbarPos('Max Threshold',title)

cv2.createTrackbar('Min Threshold', title, 27, 255, on_minThreshold)
cv2.createTrackbar('Max Threshold', title, 255, 255, on_maxThreshold)
cv2.createTrackbar('Dilate Threshold', title, 2, 10, on_dilateThreshold)

#############################
#   START MAIN LOOP         #
#############################

# loop over the frames of the video

while True:
    threshLO = 27
    threshHI = 255
    threshDI = 2

    threshLO = cv2.getTrackbarPos('Min Threshold',title)
    threshHI = cv2.getTrackbarPos('Max Threshold',title)
    threshDI = cv2.getTrackbarPos('Dilate Threshold',title)

    threshSTART()

	# grab the current frame and initialize the occupied/unoccupied
	# text
    (grabbed, frame) = camera.read()
    text = "Unoccupied"

	# if the frame could not be grabbed, then we have reached the end
	# of the video
    if not grabbed:
    	break

    # resize the frame, convert it to grayscale, and blur it
    frame = imutils.resize(frame, width=500)

    # pMOG = cv2.createBackgroundSubtractorMOG()
    # PMOG2 = cv2.createBackgroundSubtractorMOG2()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)

    # if the first frame is None, initialize it
    if firstFrame is None:
    	firstFrame = gray
    	continue

    # compute the absolute difference between the current frame and
    # first frame
    frameDelta = cv2.absdiff(firstFrame, gray)
    thresh = cv2.threshold(frameDelta, threshLO, threshHI, cv2.THRESH_BINARY)[1]

    # dilate the thresholded image to fill in holes, then find contours
    # on thresholded image
    thresh = cv2.dilate(thresh, None, iterations=threshDI)
    (_, cnts, _) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # loop over the contours
    for c in cnts:
    	# if the contour is too small, ignore it
    	if cv2.contourArea(c) < args["min_area"]:
    		continue

    	# compute the bounding box for the contour, draw it on the frame,
    	# and update the text
    	(x, y, w, h) = cv2.boundingRect(c)
    	cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
    	text = "Occupied"

    # draw the text and timestamp on the frame
    cv2.putText(frame, "Room Status: {}".format(text), (10, 20),
    	cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
    cv2.putText(frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"),
    	(10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)

    # show the frame and record if the user presses a key
    cv2.imshow(title, emptyControl)
    cv2.imshow("Security Feed", frame)
    cv2.imshow("Thresh", thresh)
    cv2.imshow("Frame Delta", frameDelta)
    key = cv2.waitKey(1) & 0xFF

    # if the `q` key is pressed, break from the lop
    if key == ord("q"):
    	break

# cleanup the camera and close any open windows
camera.release()
cv2.destroyAllWindows()
