# Project 2 - Advanced Lane Finding Project

The goals / steps of this project are the following:

* Compute the camera calibration matrix and distortion coefficients given a set of chessboard images.
* Apply a distortion correction to raw images.
* Use color transforms, gradients, etc., to create a thresholded binary image.
* Apply a perspective transform to rectify binary image ("birds-eye view").
* Detect lane pixels and fit to find the lane boundary.
* Determine the curvature of the lane and vehicle position with respect to center.
* Warp the detected lane boundaries back onto the original image.
* Output visual display of the lane boundaries and numerical estimation of lane curvature and vehicle position.

## [Rubric](https://review.udacity.com/#!/rubrics/571/view) Points

### Camera Calibration

I divided the work 3 parts : compute the correct matrix and distortion coefficients, a function applying the correction function from OpenCv (**cv2.undistort**) and a simple builder to return a closure to apply this function with more ease.

#### Compute the correction matrix and distortion coefficients [calibrationBuilder](./camera_calibration/calibrationBuilder.py)

 To compute a the correct matrix and distortion coefficients from the chessboard images inside *[./assets/camera_cal](./assets/camera_cal/)*, I first use the function [getCornersMatrix](https://github.com/jotamontecino/nd_selfdriving_project2/blob/master/camera_calibration/calibrationBuilder.py#L39-L51) to find the chessboard matrix. I [append all this matrixes](https://github.com/jotamontecino/nd_selfdriving_project2/blob/master/camera_calibration/calibrationBuilder.py#L23-L25) inside **imgPoints**(2D representation) and their 3D representation **objPoints** to use them inside [cv2.calibrateCamera](https://github.com/jotamontecino/nd_selfdriving_project2/blob/master/camera_calibration/calibrationBuilder.py#L29-L30) to get the correct matrix (**mtx**) and distortion coefficients (**dist**).

 #### Undistort function

 OpenCV exposes the function [](https://github.com/jotamontecino/nd_selfdriving_project2/blob/master/camera_calibration/undistort.py#L7). We have to simply give it the parameters found before and the image.

 For my personnal ease I choose to encapsulate it inside a [builder](https://github.com/jotamontecino/nd_selfdriving_project2/blob/master/camera_calibration/undistort.py#L5) who will return a closure with the **mtx** and **dist**, so I can simply pass it to other functions as more simple function without having to reconstruct it.
