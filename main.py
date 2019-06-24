import cv2
import matplotlib.image as mpimg
import os
import re
import numpy as np

from laneDetection.lane import Lane
from common import logger
from camera_calibration import undistortImageBuilder
from binarization import binarizeImage
from perspectiveTransformations import transformMatrix, warperBuilder


class Processor:
    def __init__(self, type="IMG"):
        self.undistortImage = undistortImageBuilder()
        self.birdViewImage = None
        self.dashCamView = None
        if (type == "IMG"):
            def createLane(currentImagePath):
                return Lane(currentImagePath)
            self.lane = createLane
        else:
            lane = Lane()
            def createLane(currentImagePath):
                return lane
            self.lane = createLane

    def processImage(self,image, currentImagePath=None):
        undistortedImage = self.undistortImage(currentImage, currentImagePath)
        binarizedImage = binarizeImage(undistortedImage, currentImagePath)
        if (self.birdViewImage is None):
            matrix, invMatrix = transformMatrix(currentImage, 450, 640, 68)
            self.birdViewImage = warperBuilder(matrix)
            self.dashCamView = warperBuilder(invMatrix)
        tmpImage = np.copy(binarizedImage).astype(np.uint8)
        binaryThreshold = np.zeros_like(tmpImage)
        binaryThreshold[(tmpImage > 0)] = 255
        warpedImage = self.birdViewImage(binaryThreshold, currentImagePath)
        if (os.environ['PYTHON_ENV'] == "debug"):
            self.birdViewImage(currentImage, currentImagePath)
        lane = self.lane(currentImagePath)
        lanePolyBirdView = lane.processImage(warpedImage)
        lanePolyDashCamView = self.dashCamView(lanePolyBirdView)
        if (os.environ['PYTHON_ENV'] == "debug"):
            path = currentImagePath.replace(".jpg", "-lanes.jpg")
            imageWithLane = cv2.addWeighted(currentImage, 1, lanePolyDashCamView, 0.5, 0)
            cv2.imwrite(path, imageWithLane)


if __name__ == '__main__':
    # logging.basicConfig(filename='myapp.log', level=logging.INFO)
    log = logger.Logger(os.environ['PYTHON_ENV'])
    log.info("Process Start")

    if (os.environ['INPUT_TYPE'] == "video"):
        pass
    else:
        controller = Processor()
        assetsFolder = os.environ['ASSETS_FOLDER']
        testImageFolder = "%s/test_images" % (assetsFolder)
        fileList = os.listdir(testImageFolder)
        for filename in fileList:
            if (re.search(r"^[a-z0-9_]+\.(jpg|png)$", filename)):
                currentImage = cv2.imread("%s/%s" % (testImageFolder, filename))
                currentImagePath = "%s/undistorted-%s" % (testImageFolder, filename)
                controller.processImage(currentImage, currentImagePath)
