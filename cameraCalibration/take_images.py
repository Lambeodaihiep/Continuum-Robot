import cv2
import numpy as np

camera_matrix1 = np.load('continuum/cameraCalibration/saveData/cam1/camera_matrix.npy')
dist_coeffs1 = np.load('continuum/cameraCalibration/saveData/cam1/dist_coeffs.npy')
rvecs1 = np.load('continuum/cameraCalibration/saveData/cam1/rvecs.npy')
tvecs1 = np.load('continuum/cameraCalibration/saveData/cam1/tvecs.npy')

camera_matrix2 = np.load('continuum/cameraCalibration/saveData/cam2/camera_matrix.npy')
dist_coeffs2 = np.load('continuum/cameraCalibration/saveData/cam2/dist_coeffs.npy')
rvecs2 = np.load('continuum/cameraCalibration/saveData/cam2/rvecs.npy')
tvecs2 = np.load('continuum/cameraCalibration/saveData/cam2/tvecs.npy')

print('Starting the Calibration. Press and maintain the space bar to exit the script\n')
print('Push (s) to save the image you want and push (c) to see next frame without saving the image')

id_image=100

# termination criteria
criteria =(cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# Call the two cameras
Cam1= cv2.VideoCapture(0) 
# Cam2= cv2.VideoCapture(1) 

while True:
    # ret2, frame2= Cam2.read()
    ret1, frame1= Cam1.read()

    # undistort camera
    frame1 = cv2.undistort(frame1, cameraMatrix=camera_matrix1, distCoeffs=dist_coeffs1)
    # frame1 = cv2.undistort(frame1, cameraMatrix=camera_matrix2, distCoeffs=dist_coeffs2)

    # gray2= cv2.cvtColor(frame2,cv2.COLOR_BGR2GRAY)
    gray1= cv2.cvtColor(frame1,cv2.COLOR_BGR2GRAY)

    # Find the chess board corners
    # ret2, corners2 = cv2.findChessboardCorners(gray2,(9,6),None)  # Define the number of chess corners (here 9 by 6) we are looking for with the right Camera
    ret1, corners1 = cv2.findChessboardCorners(gray1,(6,9),None)  # Same with the left camera
    # cv2.imshow('img2',frame2)
    cv2.imshow('img1',frame1)

    # If found, add object points, image points (after refining them)
    if (ret1 == True):
        # corners22= cv2.cornerSubPix(gray2,corners2,(11,11),(-1,-1),criteria)    # Refining the Position
        corners21= cv2.cornerSubPix(gray1,corners1,(11,11),(-1,-1),criteria)

        # Draw and display the corners
        # cv2.drawChessboardCorners(gray2,(9,6),corners22,ret2)
        cv2.drawChessboardCorners(gray1,(6,9),corners21,ret1)
        # cv2.imshow('Video2',gray2)
        cv2.imshow('Video1',gray1)

        if cv2.waitKey(0) & 0xFF == ord('s'):   # Push "s" to save the images and "c" if you don't want to
            str_id_image= str(id_image)
            print('Images ' + str_id_image + ' saved')
            cv2.imwrite('continuum/cameraCalibration/images/cam1/image1_' + str(id_image) + '.png', frame1)
            # cv2.imwrite('continuum/cameraCalibration/images/cam2/image2_' + str(id_image) + '.png', frame1)
            id_image=id_image+1
        else:
            print('Images not saved')

    # End the Programme
    if cv2.waitKey(1) & 0xFF == ord('q'):   # Push the space bar and maintan to exit this Programm
        break

# Release the Cameras
# Cam2.release()
Cam1.release()
cv2.destroyAllWindows()    