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

 For my personnal ease I choose to encapsulate it inside a [higher order function](https://github.com/jotamontecino/nd_selfdriving_project2/blob/master/camera_calibration/undistort.py#L5) who will return a closure with the **mtx** and **dist**, so I can simply pass it to other functions as more simple function without having to reconstruct it.

### Pipeline

#### Provide an example of a distortion-corrected image.

We simply apply the function **undistortImage** (we pass the image and the path to wish to save the undistorted image to have it). There is a slight difference (on the bottom corners).

| Distorted image | Undistorted Image |
|---|---|
|![alt text](https://github.com/jotamontecino/nd_selfdriving_project2/blob/master/assets/test_images/test6.jpg)|![alt text](https://github.com/jotamontecino/nd_selfdriving_project2/blob/master/assets/test_images/test6.jpg)|

#### Describe how (and identify where in your code) you used color transforms, gradients or other methods to create a thresholded binary image. Provide an example of a binary image result.

The code use to create the binary image is [here](https://github.com/jotamontecino/nd_selfdriving_project2/blob/master/binarization/__init__.py).
I first create masks for [white lines](https://github.com/jotamontecino/nd_selfdriving_project2/blob/master/binarization/colorTransformations.py#L20), [yellow lines](https://github.com/jotamontecino/nd_selfdriving_project2/blob/master/binarization/colorTransformations.py#L13) and [absolute sobel](https://github.com/jotamontecino/nd_selfdriving_project2/blob/master/binarization/sobelUtils.py#L5) for the image. I combine then using [logical_or](https://github.com/jotamontecino/nd_selfdriving_project2/blob/master/binarization/__init__.py#L13) to have a unique binary image combining the three views.
Finally I found that using a [morphological closing](https://github.com/jotamontecino/nd_selfdriving_project2/blob/master/binarization/__init__.py#L21) helps to reduce some noise with the project video.

| Test image | white mask | yellow mask |
|---|---|---|
|![test](https://github.com/jotamontecino/nd_selfdriving_project2/blob/master/assets/test_images/straight_lines1.jpg)|![white](https://github.com/jotamontecino/nd_selfdriving_project2/blob/master/assets/test_images/straight_lines1-white_thresholded.jpg)|![yellow](https://github.com/jotamontecino/nd_selfdriving_project2/blob/master/assets/test_images/straight_lines1-yellow_thresholded.jpg)|
|---|---|---|
| abs sobel image | combined mask | closed mask |
|![abs sobel](https://github.com/jotamontecino/nd_selfdriving_project2/blob/master/assets/test_images/straight_lines1-abs_sobel_thresholded.jpg)|![combined](https://github.com/jotamontecino/nd_selfdriving_project2/blob/master/assets/test_images/straight_lines1-combined_thresholded.jpg)|![closed](https://github.com/jotamontecino/nd_selfdriving_project2/blob/master/assets/test_images/straight_lines1--binary_image.jpg)|

#### Describe how (and identify where in your code) you performed a perspective transform and provide an example of a transformed image.

The code describing this part can be found inside the [perspectiveTransformations](https://github.com/jotamontecino/nd_selfdriving_project2/blob/master/perspectiveTransformations/__init__.py) module.
I first use a function to create the matrix [(**transformMatrix**)](https://github.com/jotamontecino/nd_selfdriving_project2/blob/master/perspectiveTransformations/__init__.py#L6) used for the perspective warp. I pass the Y(**yTop**) and X(**xTop**) of the central point (top center) of my quadrilateral and the width offset(**offsetWidth**) applied to X to create have my left and right points.

I created a closure around the warping function [(**warperBuilder**)](https://github.com/jotamontecino/nd_selfdriving_project2/blob/master/perspectiveTransformations/__init__.py#L23), so I only pass the transformation matrix at its creation. And I use the enclosed function(**warper**).

| Test image | Warped Image |
|---|---|
|![test](https://github.com/jotamontecino/nd_selfdriving_project2/blob/master/assets/test_images/undistorted-straight_lines1.jpg)|![warped](https://github.com/jotamontecino/nd_selfdriving_project2/blob/master/assets/test_images/undistorted-straight_lines1-birdEye.jpg)

#### Describe how (and identify where in your code) you identified lane-line pixels and fit their positions with a polynomial?

All the code relative to lane identification is locate [here](https://github.com/jotamontecino/nd_selfdriving_project2/blob/master/laneDetection/lane.py).

I use a [strategy](https://github.com/jotamontecino/nd_selfdriving_project2/blob/master/laneDetection/lane.py#L35) to apply two differents detection functions : [findLanePixels](https://github.com/jotamontecino/nd_selfdriving_project2/blob/master/laneDetection/lane.py#L123) and [findPixelWithOldFit](https://github.com/jotamontecino/nd_selfdriving_project2/blob/master/laneDetection/lane.py#L98).

I first use **findLanePixels**, to make our first detection. I use the histogram function to find some local maximum pixel concentration. We choose the [left](https://github.com/jotamontecino/nd_selfdriving_project2/blob/master/laneDetection/lane.py#L130) and [right](https://github.com/jotamontecino/nd_selfdriving_project2/blob/master/laneDetection/lane.py#L131) maximums to start our boxing. I start to iterate through my total windows (10 by default), to get all pixels inside the [left](https://github.com/jotamontecino/nd_selfdriving_project2/blob/master/laneDetection/lane.py#L175) and [right](https://github.com/jotamontecino/nd_selfdriving_project2/blob/master/laneDetection/lane.py#L181) boxes.

![Windowed](https://github.com/jotamontecino/nd_selfdriving_project2/blob/master/writeup_assets/test2-windowed.jpg)

Finally if I have enough pixels inside a box, I set the next box center as the [mean X of all the detected pixels](https://github.com/jotamontecino/nd_selfdriving_project2/blob/master/laneDetection/lane.py#L193) and add them to [detected arrays](https://github.com/jotamontecino/nd_selfdriving_project2/blob/master/laneDetection/lane.py#L200).

Before returning the selected pixels I [discriminate](https://github.com/jotamontecino/nd_selfdriving_project2/blob/master/laneDetection/lane.py#L207) the pixels by X/Y and left/right lane.

Now I have **leftx**/**lefty** and **rightx**/**righty** for all found pixels for the lane (right/left lines). I then pass them to [fitPolynomial](https://github.com/jotamontecino/nd_selfdriving_project2/blob/master/laneDetection/lane.py#L85). Inside I use the **np.polyfit** function to calculate the polynomial that fit through all selected pixels.
If found I save it to **self.rightPastFit** and **self.leftPastFit**, to use in the next frame.

After I have a first detection done by **findLanePixels**, I use **findPixelWithOldFit**. Here I calculate new lines by using the last polynomial and a margin, and I [select all pixels inside them](https://github.com/jotamontecino/nd_selfdriving_project2/blob/master/laneDetection/lane.py#L104). Finally I pass the found pixels to **fitPolynomial**.


#### Describe how (and identify where in your code) you calculated the radius of curvature of the lane and the position of the vehicle with respect to center.

[getCurvature](https://github.com/jotamontecino/nd_selfdriving_project2/blob/master/laneDetection/lane.py#L235): To calculate the Curvature, I calculate the polynomial in real space (Y * Pixel to meters ratio) for both lines and stock it. I calculate the curvature using the formula: ![function](https://github.com/jotamontecino/nd_selfdriving_project2/blob/master/writeup_assets/curveFn.svg).

[getOffsetPosition](https://github.com/jotamontecino/nd_selfdriving_project2/blob/master/laneDetection/lane.py#L245): To get the position of the vehicule with respect to center, I mean the last 5 polynomials, and calculate the X value at the bottom of the image (image height). I calculate the lane width, then the lane center from the left border and finally the difference beetwen the center of the image (image width) and the calculated lane center.

#### Provide an example image of your result plotted back down onto the road such that the lane area is identified clearly.

![Final image](https://github.com/jotamontecino/nd_selfdriving_project2/blob/master/writeup_assets/undistorted-test5-lanes.jpg)

### Pipeline (video)

#### Provide a link to your final video output. Your pipeline should perform reasonably well on the entire project video (wobbly lines are ok but no catastrophic failures that would cause the car to drive off the road!)

[Result](https://github.com/jotamontecino/nd_selfdriving_project2/blob/master/assets/test_video/result.mp4)


### Discussion

#### Briefly discuss any problems / issues you faced in your implementation of this project. Where will your pipeline likely fail? What could you do to make it more robust?

I found that creating a good binary image to work with is the most difficult part. I could make it work with the challenge videos, as I got always to much noise. That resulted on bad lane detection.

There is also the probeme of calculating a road, when the lines are not visible or even not drawn. As it often happen in city road in Europe/South America.
