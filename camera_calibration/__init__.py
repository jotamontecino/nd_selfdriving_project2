import os
import matplotlib.image as mpimg
import re

from common.logger import Logger
from camera_calibration.calibrationBuilder import calibrationMatrix
from camera_calibration.undistort import builder

# Returns a closure undistorting images with the calculated matrix
# and distortion parameters in the calibration part
def undistortImageBuilder():
    log = Logger.getInstance();
    log.info(">>> Camera calibration")
    assetsFolder = os.environ['ASSETS_FOLDER'];
    cameraCalibrationFolder = "%s/camera_cal"%(assetsFolder);
    ret, mtx, dist, rvecs, tvecs = calibrationMatrix(9, 6, cameraCalibrationFolder)
    log.info("<<< Camera calibration")
    undistortImage = builder(mtx, dist)
    if (os.environ['PYTHON_ENV'] == 'debug'):
        # Undistor all chessboard image to REVIEW them
        fileList = os.listdir(cameraCalibrationFolder)
        log.info(">>> Undistorting camera calibration images")
        for filename in fileList:
            if (re.search("^[a-z0-9]+\.(jpg|png)$", filename)):
                currentImage = mpimg.imread("%s/%s"%(cameraCalibrationFolder,filename))
                currentImagePath = "%s/undistorted-%s"%(cameraCalibrationFolder,filename)
                undistortImage(currentImage, currentImagePath);
        log.info("<<< Undistorting camera calibration images")
    return undistortImage
