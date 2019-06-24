import cv2
import numpy as np


def abs_sobel_thresh(img, orient='x', sobel_kernel=3, thresh=(20, 100)):
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
    # 6) Return this mask as your binary_output image
    return binaryThreshold.astype(bool)

# Calculate gradient magnitude
def mag_thresh(image, sobel_kernel=3, mag_thresh=(30, 100)):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    x = 1
    y = 1
    sobelx = cv2.Sobel(gray, cv2.CV_64F, x, 0)
    sobely = cv2.Sobel(gray, cv2.CV_64F, 0, y)
    abs_sobel = np.sqrt(sobelx**2 + sobely**2)
    scaled_sobel = np.uint8(255*abs_sobel/np.max(abs_sobel))
    # Apply threshold
    binaryThreshold = np.zeros_like(gray)
    binaryThreshold[(scaled_sobel > mag_thresh[0]) & (scaled_sobel < mag_thresh[1])] = 255
    return binaryThreshold


# Calculate the gradient direction
def dir_threshold(image, sobel_kernel=3, thresh=(0, np.pi/2)):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=sobel_kernel)
    sobely = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=sobel_kernel)
    abs_sobely = np.absolute(sobely)
    abs_sobelx = np.absolute(sobelx)
    gradientDirection = np.arctan2(abs_sobely, abs_sobelx)
    # Apply threshold
    binaryThreshold = np.zeros_like(gray)
    binaryThreshold[(gradientDirection > thresh[0]) & (gradientDirection < thresh[1])] = 255
    return binaryThreshold
