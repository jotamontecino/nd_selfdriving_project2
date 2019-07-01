import os
import cv2
import numpy as np
from binarization.sobelUtils import abs_sobel_thresh
from binarization.colorTransformations import yellow, white


def binarizeImage(image, pathToSave=None):
    whiteThresholded = white(np.copy(image))
    saveImage(whiteThresholded, pathToSave, "-white_thresholded.jpg")
    yellowThresholded = yellow(np.copy(image))
    saveImage(yellowThresholded, pathToSave, "-yellow_thresholded.jpg")
    combinedYellowAndWhite = np.logical_or(yellowThresholded, whiteThresholded)
    blur = cv2.GaussianBlur(image,(5,5),0)
    thresold1 = abs_sobel_thresh(blur)
    thresold2 = abs_sobel_thresh(blur, "y")
    combinedThresolds1 = np.logical_and(thresold1, thresold2)
    combinedThresolds = np.logical_or(combinedYellowAndWhite, combinedThresolds1)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    binaryImage = cv2.morphologyEx(
        combinedThresolds.astype(np.uint8),
        cv2.MORPH_CLOSE,
        kernel,
        iterations=1
    )
    return binaryImage


def saveImage(image, pathToSave, postfix):
    if (os.environ['PYTHON_ENV'] == 'debug' and pathToSave is not None):
        tmpImage = np.copy(image).astype(np.uint8)
        binaryThreshold = np.zeros_like(tmpImage)
        binaryThreshold[(tmpImage > 0)] = 255
        path = pathToSave.replace(".jpg", postfix)
        cv2.imwrite(path, binaryThreshold)
    return None
