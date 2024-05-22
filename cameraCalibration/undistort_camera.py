import numpy as np
import cv2 as cv

### Load parameter ###
camera_matrix1 = np.load('continuum/cameraCalibration/saveData/cam1/camera_matrix.npy')
dist_coeffs1 = np.load('continuum/cameraCalibration/saveData/cam1/dist_coeffs.npy')

camera_matrix2 = np.load('continuum/cameraCalibration/saveData/cam2/camera_matrix.npy')
dist_coeffs2 = np.load('continuum/cameraCalibration/saveData/cam2/dist_coeffs.npy')

### Capture video ###
cap1 = cv.VideoCapture(0, cv.CAP_DSHOW) # this is the magic!
# capLeft.set(cv.CAP_PROP_FRAME_WIDTH, 1920)
# capLeft.set(cv.CAP_PROP_FRAME_HEIGHT, 1080)
cap2 = cv.VideoCapture(1, cv.CAP_DSHOW) # this is the magic!
# capRight.set(cv.CAP_PROP_FRAME_WIDTH, 1920)
# capRight.set(cv.CAP_PROP_FRAME_HEIGHT, 1080)

while True:
    # read frames from both cameras
    ret1, frame1 = cap1.read()
    ret2, frame2 = cap2.read()

    frame1 = cv.undistort(frame1, cameraMatrix=camera_matrix1, distCoeffs=dist_coeffs1)
    frame2 = cv.undistort(frame2, cameraMatrix=camera_matrix2, distCoeffs=dist_coeffs2)

    cv.imshow('cam 1', frame1)
    cv.imshow('cam 2', frame2)
    
    # exit on 'q' key press
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

# release resources
cap1.release()
cap2.release()
cv.destroyAllWindows()
