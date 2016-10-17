# import the necessary packages
from __future__ import print_function
from imutils.video import VideoStream
import numpy as np
import argparse
import imutils
import time
import cv2

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-o", "--output", required=True,
    help="path to output video file")
ap.add_argument("-p", "--picamera", type=int, default=-1,
    help="whether or not the Raspberry Pi camera should be used")
ap.add_argument("-f", "--fps", type=int, default=20,
    help="FPS of output video")
ap.add_argument("-c", "--codec", type=str, default="MJPG",
    help="codec of output video")
args = vars(ap.parse_args())

####
# init video start / sensor warmmup #
####

print("[INFO] warming up camera...")
# vs = VideoStream(usePiCamera=args["picamera"] > 0).start()
vs = cv2.VideoCapture(0)
time.sleep(1)

cv2.namedWindow('Keypoints')



title = "Blob Detect Controls"
# cv2.namedWindow(title);
#create emtpy NumPy array to resizse trackbars
# emptyControl = np.zeros((1,500), dtype = "uint8")
# cv2.imshow(title, emptyControl)




########################################
#  SET VALUES FOR BLOG DETECTION #
#########################################


params = cv2.SimpleBlobDetector_Params()

# def paramInit(): #

# Change thresholds
# params.minThreshold = 25
# params.maxThreshold = 0

# Filter by Area

params.filterByArea = True
params.minArea = 100
params.maxArea = 1500



# Filter by Circularity
params.filterByCircularity = True
params.minCircularity = 0.0
params.maxCircularity = 1

 
# Filter by Convexity
params.filterByConvexity = True
params.minConvexity = 0.0
params.maxConvexity = 1
 
# Filter by Inertia
params.filterByInertia = True
params.minInertiaRatio = 0.0
params.maxInertiaRatio = 1



#########################################################################
# Callback function sets parameters each time trackbarpos gets updated #
########################################################################


# def on_maxThreshold(z):
#     params.maxThreshold = cv2.getTrackbarPos('Max Threshold',title)
#     params.minThreshold = cv2.getTrackbarPos('Min Threshold',title)
# #     params.minArea = cv2.getTrackbarPos('Min Filter Area',title)
# #     params.maxArea = cv2.getTrackbarPos('Max Filter Area',title)
# #     params.minCircularity = cv2.getTrackbarPos('Min Circularity',title)
#     cvDo()

def on_maxThreshold(z):
    pass




###################
# CREATE TRACKBARS #
#####################



#Create Trackbar Grayscale Threshold
# cv2.createTrackbar('Max Threshold', title, 255, 255, on_maxThreshold)
cv2.createTrackbar('Min Threshold', title, 0, 255, on_maxThreshold)
cv2.createTrackbar('Max Threshold', title, 255, 255, on_maxThreshold)


# # #Create Trackbar AREA
cv2.createTrackbar('Min Filter Area', title, 0, 4000, on_maxThreshold)
cv2.createTrackbar('Max Filter Area', title, 2500, 4000, on_maxThreshold)

# #switch = '0 : OFF \n1 : ON'
# #cv2.createTrackbar(switch, 'image', 1, 1, on_maxThreshold)

# cv2.createTrackbar('Min Circularity', title, int(0.1), int(1.0), on_maxThreshold)
# cv2.createTrackbar('Max Circularity', title, int(0.9), int(1.0), on_maxThreshold)

# cv2.createTrackbar('Min Convexity', title, int(0.1), int(1.0), on_maxThreshold)
# cv2.createTrackbar('Max Convexity', title, int(0.9), int(1.0), on_maxThreshold)

# cv2.createTrackbar('Min Inertia Ratio', title, int(0.1), int(1.0), on_maxThreshold)
# cv2.createTrackbar('Max Inertia Ratio', title, int(1.0), int(1.0), on_maxThreshold)


def paramInit():
    # Get trackbar values and set equal to params

    params.minThreshold = cv2.getTrackbarPos('Min Threshold',title)
    params.maxThreshold = cv2.getTrackbarPos('Max Threshold',title)
     
    params.minArea = cv2.getTrackbarPos('Min Filter Area',title)
    params.maxArea = cv2.getTrackbarPos('Max Filter Area', title)
    # params.filterByArea = cv2.getTrackbarPos(switch,'Keypoints')

    # params.minCircularity = cv2.getTrackbarPos('Min Circularity',title)
    # params.maxCircularity = cv2.getTrackbarPos('Max Circularity',title)

    # params.minConvexity = cv2.getTrackbarPos('Min Convexity',title)
    # params.maxConvexity = cv2.getTrackbarPos('Max Convexity',title)
   
    # params.minInertiaRatio = cv2.getTrackbarPos('Min Inertia Ratio',title)
    # params.maxInertiaRatio = cv2.getTrackbarPos('Max Inertia Ratio',title)

 



#################
# MAIN FUNCTION #
#################



def cvDo():
    while (vs.isOpened()):
        ret, frame = vs.read()
        frame = imutils.resize(frame,width=600)
        # paramInit()

        if ret == True:


                detector = cv2.SimpleBlobDetector_create(params)
                # Detect blobs.
                keypoints = detector.detect(frame)

                # Draw detected blobs as red circles.
                 # cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS ensures the size of the circle corresponds to the size of blob
                im_with_keypoints = cv2.drawKeypoints(frame, keypoints, np.array([]), (255,0,0), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

                # Show keypoints
                import thread

                cv2.imshow("Keypoints", im_with_keypoints)

                # writer.write(im_with_keypoints)

                if cv2.waitKey(60) == 27:         # wait for ESC key to exit and terminate progra,
                        cv2.destroyAllWindows()
                        vs.release()
                        writer.release()



###################
# MAIN DRAW LOOP #
##################

while (True):
	cvDo()
else:
	pass






# # loop over frames from the video stream
# while True:
#     # grab the frame from the video stream and resize it to have a
#     # maximum width of 300 pixels
#     frame = vs.read()
#     frame = imutils.resize(frame, width=300)
 
#     # check if the writer is None
#     if writer is None:
#         # store the image dimensions, initialzie the video writer,
#         # and construct the zeros array
#         (h, w) = frame.shape[:2]
#         writer = cv2.VideoWriter(args["output"], fourcc, args["fps"],
#             (w, h), True)

#     writer.write(frame)


#     # show the frames
#     cv2.imshow("Frame", frame)
#     # cv2.imshow("Output", output)
#     key = cv2.waitKey(1) & 0xFF
 
#     # if the `q` key was pressed, break from the loop
#     if key == ord("q"):
#         break
 
# # do a bit of cleanup
# print("[INFO] cleaning up...")
# cv2.destroyAllWindows()
# vs.stop()
# writer.release()


