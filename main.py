import os
from camera_calibration import calibrationBuilder

def main():
    assetsFolder = os.environ['ASSETS_FOLDER'];
    matrix = calibrationBuilder.calibrationMatrix(9, 6, "%s/camera_cal"%(assetsFolder))

main();
