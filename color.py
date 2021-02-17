import numpy as np
import argparse 
import cv2
import imutils 

def main():
	# capturing video through webcam
	
	cam = cv2.VideoCapture(1)   # 0 -> index of camera
	s, im_r = cam.read()
	if s:    # frame captured without any errors
		cv2.imwrite("filename.jpg",im_r) #save image
	
	image = cv2.imread('filename.jpg')

	'''
	Red = Land/lower
	Green = Takeoff/lift
	Blue = Left
	Yellow = Right
	'''
	instructions = color(image)
	print(instructions)

def color(image):
	hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
	kernal = np.ones((5, 5), "uint8")

	# create arrays for the RGB values
	redLowerBound = np.array([20, 20, 100], np.uint8)
	redUpperBound = np.array([40, 40, 140], np.uint8)

	greenLowerBound = np.array([10, 100, 40], np.uint8)
	greenUpperBound = np.array([30, 120, 60], np.uint8)

	blueLowerBound = np.array([100, 0, 0], np.uint8)
	blueUpperBound = np.array([255, 120, 50], np.uint8)

	yellowLowerBound = np.array([60, 130, 150], np.uint8)
	yellowUpperBound = np.array([120, 145, 180], np.uint8)

	# define color boundaries 
	boundaries = [("red", redLowerBound, redUpperBound), ("green", greenLowerBound, greenUpperBound), ("yellow", yellowLowerBound, yellowUpperBound), ("blue", blueLowerBound, blueUpperBound)]

	color_points = []

	# iterate over the colors 
	for (color, lower, upper) in boundaries:
		# create and apply color mask
		mask = cv2.inRange(image, lower, upper)
		output = cv2.bitwise_and(image, image, mask = mask)

		# convert image to BW
		grayImage = cv2.cvtColor(output, cv2.COLOR_BGR2GRAY)

		# count number of non black pixels to check if color is present after the mask was applied
		if cv2.countNonZero(grayImage) > 100:
			# find location of color
			points = cv2.findNonZero(mask)
			avg = np.mean(points, axis = 0)
			color_points.append((color, avg[0][0]))
	
	#print(color_points)
	# reorder the colors by increasing x value
	temp = 0
	for i in range(0, len(color_points)):
		for j in range(i+1, len(color_points)):
			if (color_points[i][1] > color_points[j][1]):
				temp = color_points[i]
				color_points[i] = color_points[j]
				color_points[j] = temp

	#print(color_points)

	# get the order of colors in the image
	color_order = []

	for color in color_points:
		color_order.append(color[0])

	# DEBUG: output image
	'''
	imS = cv2.resize(np.hstack([image, output]), (500,300))
	cv2.imshow("images", imS)
	cv2.waitKey(0)
	'''
	return(color_order)

if __name__ == '__main__':
    main()

