import cv2
import image_processing as imp
import numpy as np
import math
# import multi_servo
import time

# cap = cv2.VideoCapture("http://192.168.1.6:8080/video")
cap1 = cv2.VideoCapture(1, cv2.CAP_DSHOW) # this is the magic!
cap2 = cv2.VideoCapture(0, cv2.CAP_DSHOW) # this is the magic!

camera_matrix1 = np.load('continuum/cameraCalibration/saveData/cam1/camera_matrix.npy')
dist_coeffs1 = np.load('continuum/cameraCalibration/saveData/cam1/dist_coeffs.npy')
rvecs1 = np.load('continuum/cameraCalibration/saveData/cam1/rvecs.npy')
tvecs1 = np.load('continuum/cameraCalibration/saveData/cam1/tvecs.npy')

new_camera_matrix1 = np.load('continuum/cameraCalibration/saveData/cam1/new_camera_matrix.npy')
new_dist_coeffs1 = np.load('continuum/cameraCalibration/saveData/cam1/new_dist_coeffs.npy')
new_rvecs1 = np.load('continuum/cameraCalibration/saveData/cam1/new_rvecs.npy')
new_tvecs1 = np.load('continuum/cameraCalibration/saveData/cam1/new_tvecs.npy')

camera_matrix2 = np.load('continuum/cameraCalibration/saveData/cam2/camera_matrix.npy')
dist_coeffs2 = np.load('continuum/cameraCalibration/saveData/cam2/dist_coeffs.npy')
rvecs2 = np.load('continuum/cameraCalibration/saveData/cam2/rvecs.npy')
tvecs2 = np.load('continuum/cameraCalibration/saveData/cam2/tvecs.npy')

new_camera_matrix2 = np.load('continuum/cameraCalibration/saveData/cam2/new_camera_matrix.npy')
new_dist_coeffs2 = np.load('continuum/cameraCalibration/saveData/cam2/new_dist_coeffs.npy')
new_rvecs2 = np.load('continuum/cameraCalibration/saveData/cam2/new_rvecs.npy')
new_tvecs2 = np.load('continuum/cameraCalibration/saveData/cam2/new_tvecs.npy')

start_time = time.time()
l = [111, 111, 111, 100]
while True:

    # if time.time() - start_time > 4:
    #     start_time = time.time()
    #     multi_servo.move_by_length(l)
    #     temp = l[3]
    #     l[3] = l[2]
    #     l[2] = l[1]
    #     l[1] = l[0]
    #     l[0] = temp
    #     print(l)

    _, frame1 = cap1.read()
    _, frame2 = cap2.read()

    frame1 = cv2.undistort(frame1, cameraMatrix=camera_matrix1, distCoeffs=dist_coeffs1)
    frame2 = cv2.undistort(frame2, cameraMatrix=camera_matrix2, distCoeffs=dist_coeffs2)
    # frame = cv2.resize(frame, (640,480))

    blue_frame1 = imp.find_blue(frame1)
    blue_frame2 = imp.find_blue(frame2)

    red_frame1 = imp.find_red(frame1)
    red_frame2 = imp.find_red(frame2)

    frame1, Cx11, Cy11 = imp.find_color_position(frame1, blue_frame1, [0, 255], 50)
    frame1, Cx12, Cy12 = imp.find_color_position(frame1, red_frame1, [0, 255], 50)

    frame2, Cx21, Cy21 = imp.find_color_position(frame2, blue_frame2, [0, 255], 50)
    frame2, Cx22, Cy22 = imp.find_color_position(frame2, red_frame2, [0, 255], 50)
    
    cv2.line(frame2, (Cx21, Cy21), (Cx22, Cy22), (0, 250, 0), 2)
    cv2.line(frame2, (Cx21, Cy21), (Cx21+50, Cy21), (0, 250, 0), 2)

    if Cx11 == 0:
        cv2.putText(frame1, "0 rad", (Cx12+25, Cy12), cv2.FONT_HERSHEY_COMPLEX, 0.7, (0,0,0))
    else:
        cv2.line(frame1, (Cx11, Cy11), (Cx12, Cy12), (0, 250, 0), 2)
        alpha = round(math.atan((Cx12-Cx11)/abs(Cy12-Cy11)), 2)
        cv2.putText(frame1, str(alpha) + " rad", (Cx12+25, Cy12), cv2.FONT_HERSHEY_COMPLEX, 0.7, (0,0,0))

    beta = round(math.atan((Cy21-Cy22)/(Cx22-Cx21)), 2)
    cv2.putText(frame2, str(beta) + " rad", (Cx22+25, Cy22), cv2.FONT_HERSHEY_COMPLEX, 0.7, (0,0,0))
    # print(math.dist((Cx1, Cy1), (Cx2, Cy2)))

    cv2.imshow("cam 1", frame1)
    cv2.imshow("cam 2", frame2)

    if cv2.waitKey(1) == ord("q"):
        break

cap1.release()
cap2.release()
cv2.destroyAllWindows()