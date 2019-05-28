import cv2
import os


def builder(mtx, dist):
    def undistortImage( img, path=None):
        undistortedImage = cv2.undistort(img, mtx, dist, None, mtx)
        if (os.environ['PYTHON_ENV'] == 'debug' and path != None):
            cv2.imwrite(path, undistortedImage)
        return undistortedImage
    return undistortImage