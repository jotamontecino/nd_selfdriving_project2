import cv2
import os


# Returns a closure for the undistortImage with the correct matrix and
# distortion coefficients.
def builder(mtx, dist):
    def undistortImage(img, path=None):
        undistortedImage = cv2.undistort(img, mtx, dist, None, mtx)
        if (os.environ['PYTHON_ENV'] == 'debug' and path is not None):
            cv2.imwrite(path, undistortedImage)
        return undistortedImage
    return undistortImage
