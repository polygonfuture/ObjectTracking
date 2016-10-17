# Standard imports
import cv2
import numpy as np;
 
# Read image
im = cv2.imread("blob.jpg", cv2.IMREAD_GRAYSCALE)
cv2.namedWindow('Keypoints')

def on_maxThreshold(z):
    params.maxThreshold = cv2.getTrackbarPos('Max Threshold','Keypoints')
    params.minThreshold = cv2.getTrackbarPos('Min Threshold','Keypoints')
    params.minArea = cv2.getTrackbarPos('Min Filter Area','Keypoints')
    params.maxArea = cv2.getTrackbarPos('Max Filter Area','Keypoints')
    params.minCircularity = cv2.getTrackbarPos('Min Circularity','Keypoints')
    # cvDo()

def on_minThreshold(z):
    params.minThreshold = z
    cvDo()
	

# Setup SimpleBlobDetector parameters.
params = cv2.SimpleBlobDetector_Params()

# Change thresholds
params.minThreshold = 10;
params.maxThreshold = 400;

# Filter by Area.
params.filterByArea = True
params.minArea = 2500

# Filter by Circularity
params.filterByCircularity = True
params.minCircularity = 0.1

 
# Filter by Convexity
params.filterByConvexity = True
params.minConvexity = 0.87
 
# Filter by Inertia
params.filterByInertia = True
params.minInertiaRatio = 0.01


#Create Trackbar Grayscale Threshold
# cv2.createTrackbar('Max Threshold', 'Keypoints', 400, 1500, on_maxThreshold)
cv2.createTrackbar('Max Threshold', 'Keypoints', 400, 1500, lambda x: params.maxThreshold=x)

cv2.createTrackbar('Min Threshold', 'Keypoints', 10, 100, on_maxThreshold)

#Create Trackbar AREA
cv2.createTrackbar('Min Filter Area', 'Keypoints', 0, 4000, on_maxThreshold)
cv2.createTrackbar('Max Filter Area', 'Keypoints', 2500, 8000, on_maxThreshold)
#switch = '0 : OFF \n1 : ON'
#cv2.createTrackbar(switch, 'image', 1, 1, on_maxThreshold)

#cv2.createTrackbar('Filter by Circularity', 'Keypoints', , 1500, on_maxThreshold)
cv2.createTrackbar('Min Circularity', 'Keypoints', int(0.1), int(1), on_maxThreshold)


# Get trackbar values and set equal to params
params.minThreshold = cv2.getTrackbarPos('Min Threshold','Keypoints')
params.maxThreshold = cv2.getTrackbarPos('Max Threshold','Keypoints')
 
params.minArea = cv2.getTrackbarPos('Min Filter Area','Keypoints')
# params.filterByArea = cv2.getTrackbarPos(switch,'Keypoints')

params.filterByCircularity = cv2.getTrackbarPos('Filter By Circularity','Keypoints')
params.minCircularity = cv2.getTrackbarPos('Min Circularity','Keypoints')

params.filterByConvexity = cv2.getTrackbarPos('Filter by Convexity','Keypoints')
params.minConvexity = cv2.getTrackbarPos('Min Convexity','Keypoints')

params.filterByInertia = cv2.getTrackbarPos('Filter by Inertia','Keypoints')
params.minInertiaRatio = cv2.getTrackbarPos('Min Inertia Ratio','Keypoints')
 

# def input_thread(list):
#     raw_input()
#     list.append(None)

def cvDo():
#     list = []
#     thread.start_new_thread(input_thread, (list,))

#     while not list:

	# Create a detector with the parameters
	ver = (cv2.__version__).split('.')
	if int(ver[0]) < 3 :
	    detector = cv2.SimpleBlobDetector(params)
	else : 
	    detector = cv2.SimpleBlobDetector_create(params);


	# Detect blobs.
	keypoints = detector.detect(im)
 
	# Draw detected blobs as red circles.
	# cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS ensures the size of the circle corresponds to the size of blob
	im_with_keypoints = cv2.drawKeypoints(im, keypoints, np.array([]), (255,0,0), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
 
	# Show keypoints
	import thread
		
  	cv2.imshow("Keypoints", im_with_keypoints)

  	print(params.maxThreshold)
  	if cv2.waitKey(0) == 27:         # wait for ESC key to exit and terminate progra,
            cv2.destroyAllWindows()

while (True):
	cvDo()
else:
	pass


