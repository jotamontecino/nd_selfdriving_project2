import cv2
import matplotlib.image as mpimg
import os
import re

from common import logger
from camera_calibration import undistortImageBuilder

if __name__ == '__main__':
    # logging.basicConfig(filename='myapp.log', level=logging.INFO)
    log = logger.Logger(os.environ['PYTHON_ENV'])
    log.info("Process Start")

    undistortImage = undistortImageBuilder()

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
                undistortImage(currentImage, currentImagePath)
