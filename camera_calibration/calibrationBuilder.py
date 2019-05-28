import cv2
import matplotlib.image as mpimg
import numpy as np
import os
import re
from common import logger

def calibrationMatrix(rows, cols, imgFolder):
    log = logger.Logger.getInstance();
    fileList = os.listdir(imgFolder)

    # Set the default value for calibrateCamera
    objp = np.zeros((rows*cols,3), np.float32)
    objp[:,:2] = np.mgrid[0:rows,0:cols].T.reshape(-1,2)
    objPoints = [] # 3d point in real world space
    imgPoints = [] # 2d points in image plane.

    firstImage = None

    for filename in fileList:
        if (re.search("^[a-z0-9]+\.(jpg|png)$", filename)):
            try:
                currentImage = mpimg.imread("%s/%s"%(imgFolder,filename))
                corners  = getCornersMatrix(rows, cols, currentImage, filePath(imgFolder, filename))
                objPoints.append(objp)
                imgPoints.append(corners)
            except ValueError as error:
                log.warning("%s => %s"%(filename,error.args))
    # Get the width and height of the image for cv2.calibrateCamera
    imgShape = (currentImage.shape[::-1][1], currentImage.shape[::-1][2])
    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objPoints, imgPoints, imgShape, None, None)

    return ret, mtx, dist, rvecs, tvecs

def filePath(imgFolder, filename):
    def createNewFilePath(prefix):
        return "%s/%s-%s"%(imgFolder, prefix, filename)
    return createNewFilePath

def getCornersMatrix(rows, cols, img, createPrefixedFilePath):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    patternFound, corners = cv2.findChessboardCorners(gray, (rows, cols), None)
    if patternFound == True:
        #Used to refine the coner locations
        criteria = (cv2.TERM_CRITERIA_MAX_ITER + cv2.TERM_CRITERIA_EPS, 30, 0.001)
        corners = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)

        if (os.environ['PYTHON_ENV'] == "debug"):
            cv2.drawChessboardCorners(img, (rows, cols), corners, patternFound)
            cv2.imwrite(createPrefixedFilePath("chessboard"), img)
        return corners
    raise ValueError('Can\'t find a chessboard pattern')
