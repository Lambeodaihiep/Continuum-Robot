import numpy as np
import cv2 as cv
import glob

################ FIND CHESSBOARD CORNERS - OBJECT POINTS AND IMAGE POINTS #############################

chessboardSize = (6,9)
frameSize = (640,480)

# termination criteria
criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
objp = np.zeros((chessboardSize[0] * chessboardSize[1], 3), np.float32)
objp[:,:2] = np.mgrid[0:chessboardSize[0],0:chessboardSize[1]].T.reshape(-1,2)
objp = objp*25

# Arrays to store object points and image points from all the images.
objpoints = [] # 3d point in real world space
imgpoints1 = [] # 2d points in image plane.
imgpoints2 = [] # 2d points in image plane.


images1 = glob.glob('continuum/cameraCalibration/images/cam1/image1_100.png')
images2 = glob.glob('continuum/cameraCalibration/images/cam2/image2_100.png')

for img_1, img_2 in zip(images1, images2):
    img1 = cv.imread(img_1)
    img2 = cv.imread(img_2)
    gray1 = cv.cvtColor(img1, cv.COLOR_BGR2GRAY)
    gray2 = cv.cvtColor(img2, cv.COLOR_BGR2GRAY)

    # Find the chess board corners
    ret1, corners1 = cv.findChessboardCorners(img1, chessboardSize, None)
    ret2, corners2 = cv.findChessboardCorners(img2, chessboardSize, None)

    # If found, add object points, image points (after refining them)
    if ret1 and ret1 == True:
        objpoints.append(objp)

        corners1 = cv.cornerSubPix(gray1, corners1, (11,11), (-1,-1), criteria)
        imgpoints1.append(corners1)

        corners2 = cv.cornerSubPix(gray2, corners2, (11,11), (-1,-1), criteria)
        imgpoints2.append(corners2)

        # Draw and display the corners
        cv.drawChessboardCorners(img1, chessboardSize, corners1, ret1)
        cv.imshow('img 1', img1)

        cv.drawChessboardCorners(img2, chessboardSize, corners2, ret2)
        cv.imshow('img 2', img2)
        cv.waitKey(0)

cv.destroyAllWindows()

############## CALIBRATION #######################################################

ret1, cameraMatrix1, dist1, rvecs1, tvecs1 = cv.calibrateCamera(objpoints, imgpoints1, frameSize, None, None)
height1, width1, channels1 = img1.shape
newCameraMatrix1, roi_1 = cv.getOptimalNewCameraMatrix(cameraMatrix1, dist1, (width1, height1), 1, (width1, height1))

ret2, cameraMatrix2, dist2, rvecs2, tvecs2 = cv.calibrateCamera(objpoints, imgpoints2, frameSize, None, None)
height2, width2, channels2 = img2.shape
newCameraMatrix2, roi_2 = cv.getOptimalNewCameraMatrix(cameraMatrix2, dist2, (width2, height2), 1, (width2, height2))

### Save parameters ###

np.save('continuum/cameraCalibration/saveData/cam1/new_camera_matrix.npy', cameraMatrix1)
np.save('continuum/cameraCalibration/saveData/cam1/new_dist_coeffs.npy', dist1)
np.save('continuum/cameraCalibration/saveData/cam1/new_tvecs.npy', tvecs1)
np.save('continuum/cameraCalibration/saveData/cam1/new_rvecs.npy',rvecs1)

np.save('continuum/cameraCalibration/saveData/cam2/new_camera_matrix.npy', cameraMatrix2)
np.save('continuum/cameraCalibration/saveData/cam2/new_dist_coeffs.npy', dist2)
np.save('continuum/cameraCalibration/saveData/cam2/new_tvecs.npy', tvecs2)
np.save('continuum/cameraCalibration/saveData/cam2/new_rvecs',rvecs2)
