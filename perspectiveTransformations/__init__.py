import os
import cv2
import numpy as np


def transformMatrix(img, yTop, xTop, offsetWidth):
    h, w = img.shape[:2]
    src = np.float32([
        [0, h],
        [w, h],
        [xTop+offsetWidth, yTop],
        [xTop-offsetWidth, yTop]
    ])
    dst = np.float32([
        [0, h],
        [w, h],
        [w, 0],
        [0, 0]
    ])
    return cv2.getPerspectiveTransform(src, dst), cv2.getPerspectiveTransform(dst, src)


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
            path = pathToSave.replace(".jpg", "-birdEye1.jpg")
            cv2.imwrite(path, warpedImage)
        return warpedImage
    return warper
