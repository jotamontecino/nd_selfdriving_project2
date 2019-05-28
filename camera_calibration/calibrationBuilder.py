import cv2
import matplotlib.image as mpimg
import numpy as np
import os
import re

def calibrationMatrix(rows, cols, imgFolder):
    fileList = os.listdir(imgFolder)
    for filename in fileList:
        if (re.search("^[a-z0-9]+\.(jpg|png)$", filename)):
            try:
                currentImage = mpimg.imread("%s/%s"%(imgFolder,filename))
                ret, mtx, dist, rvecs, tvecs  = calculateCalibrationMatrix(rows, cols, currentImage)
            except ValueError as error:
                print(error.args, filename)

def calculateCalibrationMatrix(rows, cols, img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    patternFound, corners = cv2.findChessboardCorners(gray, (rows, cols), None)
    if patternFound == True:
        # Set the default value for calibrateCamera
        objp = np.zeros((rows*cols,3), np.float32)
        objp[:,:2] = np.mgrid[0:rows,0:cols].T.reshape(-1,2)
        objPoints = [] # 3d point in real world space
        imgPoints = [] # 2d points in image plane.

        #Used to refine the coner locations
        criteria = (cv2.TERM_CRITERIA_MAX_ITER + cv2.TERM_CRITERIA_EPS, 30, 0.001)
        corners = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)

        # cv2.drawChessboardCorners(img, (rows, cols), corners, ret)

        objPoints.append(objp)
        imgPoints.append(corners)

        return cv2.calibrateCamera(objPoints, imgPoints, gray.shape[::-1], None, None)
    raise ValueError('Can\'t find a chessboard pattern')
