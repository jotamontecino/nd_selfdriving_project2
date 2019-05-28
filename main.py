import os
import matplotlib.image as mpimg
import re

from common import logger
from camera_calibration import undistortImageBuilder

if __name__ == '__main__':
    # logging.basicConfig(filename='myapp.log', level=logging.INFO)
    log = logger.Logger(os.environ['PYTHON_ENV'])
    log.info("Process Start")
    
    undistortImage = undistortImageBuilder()
