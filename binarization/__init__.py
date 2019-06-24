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
    thresold1 = abs_sobel_thresh(image)
    saveImage(thresold1, pathToSave, "-abs_sobel_thresholded.jpg")
    combinedThresolds = np.logical_or(combinedYellowAndWhite, thresold1)
    saveImage(combinedThresolds, pathToSave, "-combined_thresholded.jpg")
    # testT = np.zeros_like(combinedThresolds, dtype=np.uint8)
    # testT[(combinedThresolds > 0)] = 1
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    binaryImage = cv2.morphologyEx(
        combinedThresolds.astype(np.uint8),
        cv2.MORPH_CLOSE,
        kernel,
        iterations=1
    )
    saveImage(binaryImage, pathToSave, "--binary_image.jpg")
    return binaryImage


def saveImage(image, pathToSave, postfix):
    if (os.environ['PYTHON_ENV'] == 'debug'):
        tmpImage = np.copy(image).astype(np.uint8)
        binaryThreshold = np.zeros_like(tmpImage)
        binaryThreshold[(tmpImage > 0)] = 255
        path = pathToSave.replace(".jpg", postfix)
        cv2.imwrite(path, binaryThreshold)
    return None
