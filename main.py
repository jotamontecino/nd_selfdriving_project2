import cv2
import os
import re
import numpy as np
from moviepy.editor import VideoFileClip

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
        self.path = None
        self.type = type
        if (type == "IMG"):
            def createLane(currentImagePath):
                return Lane(currentImagePath)
            self.lane = createLane
        else:
            assetsFolder = os.environ['ASSETS_FOLDER']
            self.path = "%s/test_video/video_index.jpg" % (assetsFolder)
            self.index = 1
            lane = Lane()
            def createLane(currentImagePath):
                return lane
            self.lane = createLane

    def processImage(self, currentImageTmp, currentImagePath=None):
        currentImage = currentImageTmp
        if (self.type == "VID"):
            currentImage = cv2.cvtColor(currentImageTmp, cv2.COLOR_RGB2BGR)
        # currentImagePath = None
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
        if (os.environ['PYTHON_ENV'] == "debug" and currentImagePath is not None):
            self.birdViewImage(currentImage, currentImagePath)
        lane = self.lane(currentImagePath)
        lanePolyBirdView, leftCurv, rightCurv, centerOffset = lane.processImage(warpedImage)
        if (lanePolyBirdView is not None):
            lanePolyDashCamView = self.dashCamView(lanePolyBirdView)
            imageWithLane = cv2.addWeighted(currentImage, 1, lanePolyDashCamView, 0.5, 0)
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(imageWithLane, 'Left curvature radius: {:.02f}m'.format(leftCurv), (840, 60), font, 0.9, (255, 255, 255), 2, cv2.LINE_AA)
            cv2.putText(imageWithLane, 'Right curvature radius: {:.02f}m'.format(rightCurv), (840, 90), font, 0.9, (255, 255, 255), 2, cv2.LINE_AA)
            cv2.putText(imageWithLane, 'Center offset: {:.02f}m'.format(centerOffset), (840, 120), font, 0.9, (255, 255, 255), 2, cv2.LINE_AA)
            if (os.environ['PYTHON_ENV'] == "debug" and currentImagePath is not None):
                path = currentImagePath.replace(".jpg", "-lanes.jpg")
                cv2.imwrite(path, imageWithLane)
            if (self.type == "VID"):
                return cv2.cvtColor(imageWithLane, cv2.COLOR_BGR2RGB)
            return imageWithLane
        else:
            if (self.type == "VID"):
                return cv2.cvtColor(currentImage, cv2.COLOR_BGR2RGB)
            return currentImage


if __name__ == '__main__':
    # logging.basicConfig(filename='myapp.log', level=logging.INFO)
    log = logger.Logger(os.environ['PYTHON_ENV'])
    log.info("Process Start")

    if (os.environ['INPUT_TYPE'] == "video"):
        assetsFolder = os.environ['ASSETS_FOLDER']
        controller = Processor("VID")
        selector = 'project'
        videoPath = "%s/test_video/video.mp4" % (assetsFolder)
        clip = VideoFileClip(videoPath).fl_image(controller.processImage)
        clip.write_videofile(videoPath.replace("video.mp4", "result.mp4"), audio=False)
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
