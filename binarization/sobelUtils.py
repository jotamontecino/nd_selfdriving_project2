import cv2
import numpy as np


def abs_sobel_thresh(img, orient='x', sobel_kernel=15, thresh=(30, 100)):
    # 2) Take the derivative in x or y given orient = 'x' or 'y'
    x = 1
    y = 0
    if orient == 'y':
        x = 0
        y = 1
    thresh_min = thresh[0]
    thresh_max = thresh[1]
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    # 3) Take the absolute value of the derivative or gradient
    sobel = cv2.Sobel(gray, cv2.CV_64F, x, y)
    abs_sobel = np.absolute(sobel)
    # 4) Scale to 8-bit (0 - 255) then convert to type = np.uint8
    scaled_sobel = np.uint8(255*abs_sobel/np.max(abs_sobel))
    # 5) Create a mask of 1's where the scaled gradient magnitude
    binaryThreshold = np.zeros_like(scaled_sobel)
    binaryThreshold[(scaled_sobel >= thresh_min) & (scaled_sobel < thresh_max)] = 1
    # binaryThreshold[(combined > 0)] = 1

    # 6) Return this mask as your binary_output image
    return binaryThreshold.astype(bool)
