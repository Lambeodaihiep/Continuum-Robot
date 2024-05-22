import numpy as np
import cv2
import image_processing as imp
import pandas as pd
import multi_servo
import time

target_point = [15, 45, 90]
tendon_length = [90, 90, 90, 90]
sum_error = [0, 0]
error = [0, 0]
prev_error = [0, 0]
Kp = [0.6, 0.5]
Ki = [0.2, 0.1]
Kd = [0.01, 0.04]
multi_servo.move_by_length(tendon_length)

### Load parameter ###
camera_matrix1 = np.load('continuum/cameraCalibration/saveData/cam1/camera_matrix.npy')
dist_coeffs1 = np.load('continuum/cameraCalibration/saveData/cam1/dist_coeffs.npy')
rvecs1 = np.load('continuum/cameraCalibration/saveData/cam1/rvecs.npy')
tvecs1 = np.load('continuum/cameraCalibration/saveData/cam1/tvecs.npy')

camera_matrix2 = np.load('continuum/cameraCalibration/saveData/cam2/camera_matrix.npy')
dist_coeffs2 = np.load('continuum/cameraCalibration/saveData/cam2/dist_coeffs.npy')
rvecs2 = np.load('continuum/cameraCalibration/saveData/cam2/rvecs.npy')
tvecs2 = np.load('continuum/cameraCalibration/saveData/cam2/tvecs.npy')

new_camera_matrix1 = np.load('continuum/cameraCalibration/saveData/cam1/new_camera_matrix.npy')
new_dist_coeffs1 = np.load('continuum/cameraCalibration/saveData/cam1/new_dist_coeffs.npy')
new_rvecs1 = np.load('continuum/cameraCalibration/saveData/cam1/new_rvecs.npy')
new_tvecs1 = np.load('continuum/cameraCalibration/saveData/cam1/new_tvecs.npy')

new_camera_matrix2 = np.load('continuum/cameraCalibration/saveData/cam2/new_camera_matrix.npy')
new_dist_coeffs2 = np.load('continuum/cameraCalibration/saveData/cam2/new_dist_coeffs.npy')
new_rvecs2 = np.load('continuum/cameraCalibration/saveData/cam2/new_rvecs.npy')
new_tvecs2 = np.load('continuum/cameraCalibration/saveData/cam2/new_tvecs.npy')

# check1 = [[125,0,0], [-125,0,0], [0,125,0], [0,-125,0], [125,125,0], [125,-125,0], [-125,125,0], [-125,-125,0]]
# check2 = [[125,0,0], [-125,0,0], [0,125,0], [0,250,0], [125,125,0], [125,250,0], [-125,250,0], [-125,-250,0]]
origin1=(333, 240)
origin2=(112, 240)

# position data
data_XYZ_1 = pd.read_excel("continuum/image_processing/data/data_XYZ.xlsx", sheet_name="frame 1")
data_XYZ_2 = pd.read_excel("continuum/image_processing/data/data_XYZ.xlsx", sheet_name="frame 2")

### Capture video ###
cap1 = cv2.VideoCapture(0, cv2.CAP_DSHOW) # this is the magic!
# capLeft.set(cv.CAP_PROP_FRAME_WIDTH, 1920)
# capLeft.set(cv.CAP_PROP_FRAME_HEIGHT, 1080)
cap2 = cv2.VideoCapture(1, cv2.CAP_DSHOW) # this is the magic!
# capRight.set(cv.CAP_PROP_FRAME_WIDTH, 1920)
# capRight.set(cv.CAP_PROP_FRAME_HEIGHT, 1080)

# draw coordinate axes
img_points1, x_points1, y_points1 = imp.get_coordinate_axes(new_camera_matrix1, new_dist_coeffs1, new_rvecs1[0], new_tvecs1[0], axis_length=125, origin=origin1, axis="x")
img_points2, x_points2, y_points2 = imp.get_coordinate_axes(new_camera_matrix2, new_dist_coeffs2, new_rvecs2[0], new_tvecs2[0], axis_length=125, origin=origin2, axis="y")

data_real = []

# def click_event(event, x, y, flags, params): 
#     # checking for left mouse clicks 
#     if event == cv2.EVENT_LBUTTONDOWN: 
#         data_real.append([X, Y, Z])
#         print(X, Y, Z)
    # if event == cv2.EVENT_RBUTTONDOWN:
    # if event == cv2.EVENT_MBUTTONDOWN:

send_time = start_time = time.time()

while True:
    # read frames from both cameras
    _, frame1 = cap2.read()
    _, frame2 = cap1.read()

    # undistort camera
    frame1 = cv2.undistort(frame1, cameraMatrix=camera_matrix1, distCoeffs=dist_coeffs1)
    frame2 = cv2.undistort(frame2, cameraMatrix=camera_matrix2, distCoeffs=dist_coeffs2)

    # find color point
    # blue_frame1 = imp.find_blue(frame1)
    # blue_frame2 = imp.find_blue(frame2)

    red_frame1 = imp.find_red(frame1)
    red_frame2 = imp.find_red(frame2)

    # # preprocessing
    # frame1, Cx_blue_1, Cy_blue_1 = imp.find_color_position(frame1, blue_frame1, [0, 255], 50)
    # frame2, Cx_blue_2, Cy_blue_2 = imp.find_color_position(frame2, blue_frame2, [0, 255], 50)

    frame1, pos1, Cx_red_1, Cy_red_1 = imp.find_red_position(frame1, red_frame1, [0, 255], 10, data_XYZ_1, axis="x")
    frame2, pos2, Cx_red_2, Cy_red_2 = imp.find_red_position(frame2, red_frame2, [0, 255], 10, data_XYZ_2, axis="y")

    X, Y, Z = imp.calculate_real_position((0,835,0), (-710,125,0), (0,270,float(pos1[0])), (float(pos1[1]),270,0), (-145,125,float(pos2[0])), (-145,float(pos2[1]),0))

    prev_error = error
    error = imp.cal_error_phi_and_theta(target_point, [X, Y, Z])
    print("phi_error = ", end="")
    print(round(error[0], 3), end = ", ")
    print("theta_error = ", end="")
    print(round(error[1], 3), end = ", ")
    delta_t = (time.time() - start_time) / 1000
    start_time = time.time()
    U = imp.PID(sum_error, error, prev_error, Kp, Ki, Kd, delta_t, (30, 18))
    # print(round(U[0], 2), round(U[1], 2), end=" ")
    current_phi, current_theta = imp.cal_phi_and_theta([X, Y, Z])
    current_phi, current_theta = imp.update_phi_and_theta(current_phi, current_theta, U)
    # print(round(current_phi, 2), round(current_theta, 2), end=" ")

    tendon_length = imp.update_tendon_length(current_phi, current_theta, tendon_length)
    multi_servo.move_by_length(tendon_length) # điều chỉnh lại góc động cơ
    print(tendon_length)

    if time.time() - send_time > 0.8:

    #     # data_real.append([X, Y, Z])
    #     # print(X, Y, Z)
    #     multi_servo.move(XX[ii%3], YY[ii%3], ZZ[ii%3])
    #     ii += 1
        multi_servo.move_by_length(tendon_length)
        send_time = time.time()
    
    ### Hiển thị thông tin lên khung hình

    frame1 = imp.draw_coordinate_axes(frame1, img_points1, x_points1, y_points1, axis="x")
    frame2 = imp.draw_coordinate_axes(frame2, img_points2, x_points2, y_points2, axis="y")

    # cv2.line(frame2, (Cx_blue_2, Cy_blue_2), (Cx_red_2, Cy_red_2), (0, 250, 0), 2)
    # cv2.line(frame2, (Cx_blue_2-100, Cy_blue_2), (Cx_blue_2+100, Cy_blue_2), (0, 250, 0), 2)

    cv2.putText(frame1, str(Y)+","+str(X), (Cx_red_1,Cy_red_1-25), cv2.FONT_HERSHEY_COMPLEX, 0.6, (0,0,0), 1)
    cv2.putText(frame2, str(Y)+","+str(Z), (Cx_red_2,Cy_red_2-25), cv2.FONT_HERSHEY_COMPLEX, 0.6, (0,0,0), 1)
    cv2.putText(frame1, "target: " + str(target_point), (10, 30), cv2.FONT_HERSHEY_COMPLEX, 0.6, (0,0,0), 1)

    cv2.imshow('cam 1', frame1)
    # cv2.setMouseCallback('cam 1', click_event)
    cv2.imshow('cam 2', frame2)
    
    # exit on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# release resources
cap1.release()
cap2.release()
cv2.destroyAllWindows()

# data = pd.DataFrame(data_real)
# writer = pd.ExcelWriter("continuum/image_processing/data/trajectory/10_85_-5_50.xlsx")
# data.to_excel(writer, sheet_name="data", index=False, columns=None, startcol=4)

# writer.close()