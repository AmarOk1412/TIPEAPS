import numpy as np
import cv2

im = cv2.imread('test2.jpg')
im = cv2.imread('seb.png')
# Convert BGR to HSV
hsv = cv2.cvtColor(im, cv2.COLOR_BGR2HSV)


# define range of blue color in HSV
lower_blue = np.array([120, 0,50])
upper_blue = np.array([140,100,100])

# Threshold the HSV image to get only blue colors
mask = cv2.inRange(hsv, lower_blue, upper_blue)

print(np.count_nonzero(mask))

# Bitwise-AND mask and original image
res = cv2.bitwise_and(im,im, mask= mask)
cv2.imwrite('fin4.jpg',res)

gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
ret,thresh = cv2.threshold(gray,50,255,cv2.THRESH_BINARY)
print(type(thresh))
print(np.count_nonzero(thresh))
cv2.imwrite('t.png',thresh)
