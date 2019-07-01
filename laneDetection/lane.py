import os
import cv2
import numpy as np


class Lane:
    """
    Lane definition
    """

    def __init__(self, pathToSave=None, buffer_len=10):
        self.CurvatureRadius = None
        self.pathToSave = pathToSave
        self.env = os.environ['PYTHON_ENV']
        self.leftPastFit = None
        self.rightPastFit = None

    def processImage(self, image):
        leftX = None
        leftY = None
        rightX = None
        rightY = None
        windowedImage = None
        if (self.leftPastFit is not None or self.rightPastFit is not None):
            leftX, leftY, rightX, rightY, windowedImage = self.findPixelWithOldFit(image)
        else:
            leftX, leftY, rightX, rightY, windowedImage = self.findLanePixels(image)
        if (self.env == "debug" and self.pathToSave is not None):
            path = self.pathToSave.replace(".jpg", "-windowed.jpg")
            cv2.imwrite(path, windowedImage)
        leftFit, rightFit = self.fitPolynomial(leftX, leftY, rightX, rightY)
        if (leftFit is not None and rightFit is not None):
            laneImage, laneMask = self.drawLane(image, leftFit, rightFit)
            if (self.env == 'debug' and self.pathToSave is not None):
                path = self.pathToSave.replace(".jpg", "-laneDrawn.jpg")
                cv2.imwrite(path, laneImage)
            return laneMask
        return None

    def drawLane(self, image, leftFit, rightFit):
        h, w = image.shape
        plotY = np.linspace(0, h - 1, h)
        leftFitX = leftFit[0]*plotY**2 + leftFit[1]*plotY + leftFit[2]
        leftPoints = self.drawLine(leftFitX, plotY)
        rightFitX = rightFit[0]*plotY**2 + rightFit[1]*plotY + rightFit[2]
        rightPoints = self.drawLine(rightFitX, plotY)
        laneSurface = self.drawPoly(leftFitX, rightFitX, plotY)
        colorImage = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
        emptyColorMask = np.zeros_like(colorImage)
        laneMask = cv2.fillPoly(emptyColorMask, [np.int32(leftPoints)], (20, 206, 33))
        laneMask1 = cv2.fillPoly(laneMask, [np.int32(rightPoints)], (11, 87, 193))
        laneMask2 = cv2.fillPoly(laneMask1, [np.int32(laneSurface)], (201, 2, 25))
        imageWithLane = cv2.addWeighted(colorImage, 0.8, laneMask2, 0.3, 0)
        return imageWithLane, laneMask

    def drawPoly(self, lineLeft, lineRight, plotY, width=50):
        rightBorder = lineRight - width//2
        leftBorder = lineLeft + width//2
        # We create the point on the left side of the lane (polygon)
        leftPoints = np.array(list(zip(leftBorder, plotY)))
        # We create the points of the right side, we invert them to
        # close the polygon
        rightPoints = np.array(np.flipud(list(zip(rightBorder, plotY))))
        return np.vstack([leftPoints, rightPoints])

    def drawLine(self, line, plotY):
        return self.drawPoly(line, line, plotY)

    def fitPolynomial(self, leftx, lefty, rightx, righty, minpix=0):
        try:
            leftFit = self.leftPastFit
            rightFit = self.rightPastFit
            if ( leftx.size > minpix ):
                leftFit = np.polyfit(lefty, leftx, 2)
                self.leftPastFit = leftFit
            if ( rightx.size > minpix ):
                rightFit = np.polyfit(righty, rightx, 2)
                self.rightPastFit = rightFit
            return leftFit, rightFit
        except ValueError:
            return None, None

    def findPixelWithOldFit(self, binary_warped):
        margin = 100
        if (self.leftPastFit is not None and self.rightPastFit is not None):
            nonzero = binary_warped.nonzero()
            nonzeroy = np.array(nonzero[0])
            nonzerox = np.array(nonzero[1])
            leftLaneInds = (
                (nonzerox > (self.leftPastFit[0]*(nonzeroy**2) + self.leftPastFit[1]*nonzeroy +
        self.leftPastFit[2] - margin)) &
                (nonzerox < (self.leftPastFit[0]*(nonzeroy**2) +
        self.leftPastFit[1]*nonzeroy + self.leftPastFit[2] + margin))
            )

            right_lane_inds = ((nonzerox > (self.rightPastFit[0]*(nonzeroy**2) + self.rightPastFit[1]*nonzeroy +
        self.rightPastFit[2] - margin)) & (nonzerox < (self.rightPastFit[0]*(nonzeroy**2) +
        self.rightPastFit[1]*nonzeroy + self.rightPastFit[2] + margin)))

            leftx = nonzerox[leftLaneInds]
            lefty = nonzeroy[leftLaneInds]
            rightx = nonzerox[right_lane_inds]
            righty = nonzeroy[right_lane_inds]
            return leftx, lefty, rightx, righty, binary_warped
        else:
            print("TUTUTUT")
        # else:
        #     raise Error

    def findLanePixels(self, binary_warped, nwindows = 10, margin = 100, minpix = 50, windowsColor=(0,255,255)):
        height, width = binary_warped.shape
        histogram = np.sum(binary_warped[height//2:-30, :], axis=0)
        out_img = np.dstack((binary_warped, binary_warped, binary_warped))
        # Find the peak of the left and right halves of the histogram
        # These will be the starting point for the left and right lines
        midPoint = np.int(histogram.shape[0]//2)
        leftXBottom = np.argmax(histogram[:midPoint])
        rightXBottom = np.argmax(histogram[midPoint:]) + midPoint

        # Set height of windows - based on nwindows above and image shape
        window_height = np.int(binary_warped.shape[0]//nwindows)
        # Identify the x and y positions of all nonzero pixels in the image
        nonzero = binary_warped.nonzero()
        nonzeroy = np.array(nonzero[0])
        nonzerox = np.array(nonzero[1])
        # Current positions to be updated later for each window in nwindows
        leftXCurrent = leftXBottom
        rightXCurrent = rightXBottom

        # Create empty lists to receive left and right lane pixel indices
        left_lane_inds = []
        right_lane_inds = []

        # Step through the windows one by one
        for window in range(nwindows):
            # Find the X/Y for the 4 points defining the window
            win_y_low = binary_warped.shape[0] - (window+1)*window_height
            win_y_high = binary_warped.shape[0] - window*window_height

            win_xleft_low = leftXCurrent - margin
            win_xleft_high = leftXCurrent + margin
            win_xright_low = rightXCurrent - margin
            win_xright_high = rightXCurrent + margin

            # Draw the windows on the visualization image
            cv2.rectangle(
                out_img,
                (win_xleft_low, win_y_low),
                (win_xleft_high, win_y_high),
                windowsColor,
                2
            )
            cv2.rectangle(
                out_img,
                (win_xright_low, win_y_low),
                (win_xright_high, win_y_high),
                windowsColor,
                2
            )

            # Identify the nonzero pixels in x and y within the window
            good_left_inds = (
                (nonzeroy >= win_y_low) &
                (nonzeroy < win_y_high) &
                (nonzerox >= win_xleft_low) &
                (nonzerox < win_xleft_high)
            ).nonzero()[0]
            good_right_inds = (
                (nonzeroy >= win_y_low) &
                (nonzeroy < win_y_high) &
                (nonzerox >= win_xright_low) &
                (nonzerox < win_xright_high)
            ).nonzero()[0]

            # Append these indices to the lists
            left_lane_inds.append(good_left_inds)
            right_lane_inds.append(good_right_inds)
            ### TO-DO: If you found > minpix pixels, recenter next window ###
            if len(good_left_inds) > minpix:
                leftXCurrent = np.int(np.mean(nonzerox[good_left_inds]))
            if len(good_right_inds) > minpix:
                rightXCurrent = np.int(np.mean(nonzerox[good_right_inds]))
            ### (`right` or `leftx_current`) on their mean position ###

        # Concatenate the arrays of indices (previously was a list of lists of pixels)
        try:
            left_lane_inds = np.concatenate(left_lane_inds)
            right_lane_inds = np.concatenate(right_lane_inds)
        except ValueError:
            # Avoids an error if the above is not implemented fully
            pass

        # Extract left and right line pixel positions
        leftx = nonzerox[left_lane_inds]
        lefty = nonzeroy[left_lane_inds]
        rightx = nonzerox[right_lane_inds]
        righty = nonzeroy[right_lane_inds]

        return leftx, lefty, rightx, righty, out_img
