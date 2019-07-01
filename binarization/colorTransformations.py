import cv2
import numpy as np


def hlsTransformation(image, minThresold, maxThresold):
    hlsImage = cv2.cvtColor(image, cv2.COLOR_BGR2HLS)
    minThreshold = np.all(hlsImage > minThresold, axis=2)
    maxThreshold = np.all(hlsImage < maxThresold, axis=2)
    output = np.logical_and(minThreshold, maxThreshold)
    return output


def yellow(image):
    yellowMinThresholds = np.array([10, 50, 50], dtype=np.uint8)
    yellowMaxThresholds = np.array([70, 255, 255], dtype=np.uint8)
    combinedImg = hlsTransformation(image, yellowMinThresholds, yellowMaxThresholds)
    return combinedImg


def white(image):
    hlsImage = cv2.cvtColor(image, cv2.COLOR_BGR2HLS)
    Lchannel = hlsImage[:,:,1]
    whiteColorImage = cv2.inRange(Lchannel, 220, 255)
    return whiteColorImage
