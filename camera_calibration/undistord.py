def undistorImageBuilder(mtx, dist):
    def undistorImage( img):
        return cv2.undistort(img, mtx, dist, None, mtx)
    return undistorImage;

# imgInnerCorners = [(9, 5), (9,5), (9,6), (9,6),
#                    (9,6), (9,6), (9,6), (9,6)
#                   , (9,6), (9,6), (9,6), (9,6)
#                   , (9,6), (9,6), (9,6), (9,6)
#                   , (9,6), (9,6), (9,6), (9,6)]
# currentImg = 0
# imageList = []

# for i in range(0, len(fileList)):
#     print("handling camera %d"%i, fileList[i])
#     currentFilename = fileList[i].replace(".jpg", ".png")
#     currentImage = mpimg.imread("camera_cal/%s" % (fileList[i]))
#     cornersDefs = imgInnerCorners[i]
#     try:
#         ret, mtx, dist, rvecs, tvecs  = calculateCalibrationMatrix(cornersDefs[0], cornersDefs[1], currentImage)
#         undistordedImg = undistorImages(mtx, dist, currentImage)
#         imageList.append(undistordedImg)
#         mpimg.imsave("camera_cal_undistorded/%s"%currentFilename, undistordedImg)
#     except ValueError as error:
#         print(error.args, i, fileList[i])
