import numpy as np
import cv2
import image_processing as imp
import draw_coordinate as drc

### Load parameter ###
camera_matrix1 = np.load('continuum/cameraCalibration/saveData/cam1/camera_matrix.npy')
dist_coeffs1 = np.load('continuum/cameraCalibration/saveData/cam1/dist_coeffs.npy')
rvecs1 = np.load('continuum/cameraCalibration/saveData/cam1/rvecs.npy')
tvecs1 = np.load('continuum/cameraCalibration/saveData/cam1/tvecs.npy')

camera_matrix2 = np.load('continuum/cameraCalibration/saveData/cam2/camera_matrix.npy')
dist_coeffs2 = np.load('continuum/cameraCalibration/saveData/cam2/dist_coeffs.npy')
rvecs2 = np.load('continuum/cameraCalibration/saveData/cam2/rvecs.npy')
tvecs2 = np.load('continuum/cameraCalibration/saveData/cam2/tvecs.npy')

frame1 = cv2.imread("continuum/cameraCalibration/images/cam1/image1_0.png")
frame2 = cv2.imread("continuum/cameraCalibration/images/cam2/image2_0.png")

# undistort camera
frame1 = cv2.undistort(frame1, cameraMatrix=camera_matrix1, distCoeffs=dist_coeffs1)
frame2 = cv2.undistort(frame2, cameraMatrix=camera_matrix2, distCoeffs=dist_coeffs2)

rvecs_1 = np.array([[ 0.05766944],
                    [ 0.0036206 ],
                    [-1.56802632]])
tvecs_1 = np.array([[-57.62255196],
                    [103.91611876],
                    [826.03275086]])

rvecs_2 = np.array([[ 0.01840342],
                    [ 0.02745615],
                    [-1.5690035 ]])
tvecs_2 = np.array([[-92.50277214],
                    [ 75.3100174 ],
                    [515.28022294]])
# img_points1, x_points1, y_points1 = drc.get_coordinate_axes(camera_matrix1, dist_coeffs1, rvecs_1, tvecs_1, axis_length=250, origin=(110, 450))
# img_points2, x_points2, y_points2 = drc.get_coordinate_axes(camera_matrix2, dist_coeffs2, rvecs_2, tvecs_2, axis_length=250, origin=(110, 450))

# img_points1, x_points1, y_points1 = drc.get_coordinate_axes(camera_matrix1, dist_coeffs1, rvecs1[0], tvecs1[0], axis_length=250, origin=(110, 450))
# img_points2, x_points2, y_points2 = drc.get_coordinate_axes(camera_matrix2, dist_coeffs2, rvecs2[0], tvecs2[0], axis_length=250, origin=(110, 450))

# draw coordinate axes
# frame1 = drc.draw_coordinate_axes(frame1, img_points1, x_points1, y_points1)
# frame2 = drc.draw_coordinate_axes(frame2, img_points2, x_points2, y_points2)

frame1 = drc.draw_coordinate_axes_no_fix(frame1, camera_matrix1, dist_coeffs1, rvecs1[0], tvecs1[0], axis_length=225)
frame2 = drc.draw_coordinate_axes_no_fix(frame2, camera_matrix2, dist_coeffs2, rvecs2[0], tvecs2[0], axis_length=225)

# frame1 = cv2.undistort(frame1, cameraMatrix=camera_matrix1, distCoeffs=dist_coeffs1)
# frame2 = cv2.undistort(frame2, cameraMatrix=camera_matrix2, distCoeffs=dist_coeffs2)

cv2.imshow('cam 1', frame1)
cv2.imshow('cam 2', frame2)

print(rvecs1[0])
print(tvecs1[0])
print(rvecs2[0])
print(tvecs2[0])

cv2.waitKey(0)
cv2.destroyAllWindows()
