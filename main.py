import cv2
import matplotlib.image as mpimg
import os
import re
import numpy as np

from laneDetection import laneDetector
from common import logger
from camera_calibration import undistortImageBuilder
from binarization import binarizeImage
from perspectiveTransformations import transformMatrix, warperBuilder

if __name__ == '__main__':
    # logging.basicConfig(filename='myapp.log', level=logging.INFO)
    log = logger.Logger(os.environ['PYTHON_ENV'])
    log.info("Process Start")

    undistortImage = undistortImageBuilder()
    birdViewImage = None
    dashCamView = None

    if (os.environ['INPUT_TYPE'] == "video"):
        pass
    else:
        assetsFolder = os.environ['ASSETS_FOLDER']
        testImageFolder = "%s/test_images" % (assetsFolder)
        fileList = os.listdir(testImageFolder)
        for filename in fileList:
            if (re.search(r"^[a-z0-9_]+\.(jpg|png)$", filename)):
                currentImage = cv2.imread("%s/%s" % (testImageFolder, filename))
                currentImagePath = "%s/undistorted-%s" % (testImageFolder, filename)
                undistortedImage = undistortImage(currentImage, currentImagePath)
                binarizedImage = binarizeImage(undistortedImage, "%s/%s" % (testImageFolder, filename))
                if (birdViewImage is None):
                    matrix, invMatrix = transformMatrix(currentImage, 450, 640, 68)
                    birdViewImage = warperBuilder(matrix)
                    dashCamView = warperBuilder(invMatrix)
                tmpImage = np.copy(binarizedImage).astype(np.uint8)
                binaryThreshold = np.zeros_like(tmpImage)
                binaryThreshold[(tmpImage > 0)] = 255
                warpedImage = birdViewImage(binaryThreshold, "%s/%s" % (testImageFolder, filename))
                if (os.environ['PYTHON_ENV'] == "debug"):
                    birdViewImage(currentImage, currentImagePath)
                lanePolyBirdView = laneDetector(warpedImage, "%s/%s" % (testImageFolder, filename))
                lanePolyDashCamView = dashCamView(lanePolyBirdView)
                if (os.environ['PYTHON_ENV'] == "debug"):
                    path = currentImagePath.replace(".jpg", "-lanes.jpg")
                    imageWithLane = cv2.addWeighted(currentImage, 1, lanePolyDashCamView, 0.5, 0)
                    cv2.imwrite(path, imageWithLane)
