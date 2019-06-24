import os
import cv2
import numpy as np


def transformMatrix(img):
    offset = 0
    xl = 0
    y = 450
    xr = 1280
    width = 640
    offsetWidth = 68
    src = np.float32([
        [xl, img.shape[0]],
        [xr, img.shape[0]],
        [width-offsetWidth, y],
        [width+offsetWidth, y]
    ])
    dst = np.float32([
        [offset, img.shape[0]],
        [img.shape[1]-offset, img.shape[0]],
        [offset, offset],
        [img.shape[1]-offset, offset]
    ])
    return cv2.getPerspectiveTransform(src, dst)


def warperBuilder(matrix):
    def warper(img, pathToSave=None):
        img_size = (img.shape[1], img.shape[0])
        # img_size = (1280, 720)
        warpedImage = cv2.warpPerspective(
            img,
            matrix,
            img_size,
            flags=cv2.INTER_LINEAR
        )
        if (os.environ['PYTHON_ENV'] == 'debug' and pathToSave is not None):
            path = pathToSave.replace(".jpg", "-birdEye.jpg")
            cv2.imwrite(path, warpedImage)
    return warper
